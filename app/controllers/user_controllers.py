from flask import jsonify
from flask_smorest import Blueprint
from app.services.user_services import create_user, get_all_users
from app.schemas.user_schema import UserCreateSchema  # Using your Marshmallow schema

bp = Blueprint(
    "users", "users", url_prefix="/api/v1/users", description="User operations"
)


@bp.route("/test", methods=["GET"])
def test_endpoint_main():
    """Test endpoint to verify API functionality"""
    return jsonify({"message": "success"}), 200


@bp.route("", methods=["POST"])
@bp.arguments(
    UserCreateSchema
)  # Validates and deserializes incoming JSON using Marshmallow
@bp.response(201, description="User created successfully")
def create_user_main(new_data):
    """
    Create a new user and return success.
    new_data: dict - validated data from request payload.
    """
    return create_user(new_data)


@bp.route("", methods=["GET"])
def get_all_users_main():
    return get_all_users()
