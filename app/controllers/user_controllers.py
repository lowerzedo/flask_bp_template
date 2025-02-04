from app.services.user_services import create_user
from app.utils.auth_decorator import acl_required_to_login


@acl_required_to_login(["ACL_ADMIN"])
def create_user_main(**kwargs):
    return create_user(**kwargs)
