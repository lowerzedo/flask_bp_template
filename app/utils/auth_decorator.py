from functools import wraps
from typing import Callable, Any
from flask import request, jsonify


def acl_required_to_login(allowed_acl):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return (
                    microsoft_auth(allowed_acl, f, *args, **kwargs)
                    if "ticket" not in request.args
                    else cas_auth(allowed_acl, f, *args, **kwargs)
                )
            except Exception as e:
                logger.error({"Error": e})
                return (
                    jsonify({"error": "An error has occurred during authentication"}),
                    500,
                )

        return wrapper

    return decorator


def microsoft_auth(allowed_acl, f, *args, **kwargs):
    try:
        # Extract the token from the Authorization header
        token = request.headers.get("Authorization", default=None)
        if not token:
            return jsonify({"error": "Token not provided"}), 401

        # Send a request to the Microsoft auth service to validate the token
        resp = requests.get(
            f"{auth_url}/login?user_groups=True", headers={"Authorization": token}
        )

        # Check if the authentication was successful
        if resp.status_code != 200:
            print(resp.status_code, resp.text)
            try:
                error = json.loads(resp.text)
                return jsonify(error), resp.status_code
            except json.JSONDecodeError as e:
                print(e)
                return (
                    jsonify(
                        {
                            "error": "An error occurred while decoding the authentication response"
                        }
                    ),
                    500,
                )

        # Extract user information from the response
        user_data = json.loads(resp.text)["msg"]
        samaccount = user_data["onPremisesSamAccountName"]
        groups = user_data.get("groups", [])

        # Call get_user_access to verify if user has the necessary permissions
        access_details = get_user_access({"memberOf": groups}, "microsoft")
        user_access_allowed = any(acl in allowed_acl for acl in access_details["ACL"])
        for access in access_details["ACL"]:
            for acl in allowed_acl:
                if acl in access:
                    kwargs["accesslist"] = access_details
                    kwargs["samaccount"] = samaccount
                    return f(*args, **kwargs)
        if not user_access_allowed:
            return make_response(
                jsonify(
                    {
                        "errors": [
                            {
                                "reason": "Unauthorized",
                                "message": "You do not have the necessary permissions to access this resource",
                                "code": 401,
                            }
                        ]
                    }
                ),
                401,
            )

        return f(*args, **kwargs)
    except Exception as e:
        print(e)
        return jsonify({"error": "An error has occurred during authentication"}), 500


def cas_auth(allowed_acl, f, *args, **kwargs):
    if "ticket" not in request.args:
        return redirect(CAS_URLs + "/cas/login?service=" + request.base_url, code=302)
    resp = requests.get(
        CAS_VALIDATE_URL,
        params={
            "format": "json",
            "service": request.base_url,
            "ticket": str(jinja2.escape(request.args.get("ticket"))),
        },
    )
    if resp.status_code != 200:
        return (
            jsonify(
                {"msg": "Something went wrong while we tried to authenticate you."}
            ),
            500,
        )
    service_response = resp.json()["serviceResponse"]
    if "authenticationFailure" in service_response:
        if service_response["authenticationFailure"]["code"] == "INVALID_TICKET":
            return jsonify({"msg": "CAS Service Ticket is invalid"}), 401
        return jsonify({"msg": "Authentication Failed."}), 500
    attributes = service_response["authenticationSuccess"]["attributes"]
    for k in attributes:
        if k in cas_attrs:
            kwargs["cas:" + k] = attributes[k][0]

    accessList = get_user_access(attributes, "cas")
    for access in accessList["ACL"]:
        for acl in allowed_acl:
            if acl in access:
                kwargs["accesslist"] = accessList
                return f(*args, **kwargs)
    return make_response(
        jsonify(
            {
                "errors": [
                    {
                        "reason": "Unauthorized",
                        "message": "Unauthorized to access this resource",
                        "code": 401,
                    }
                ]
            }
        ),
        401,
    )


def get_staff_id(**kwargs):
    staff_id = (
        kwargs["cas:sAMAccountName"]
        if "cas:sAMAccountName" in kwargs
        else kwargs["samaccount"]
    )
    return staff_id
