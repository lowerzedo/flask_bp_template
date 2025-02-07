from app.services.user_services import create_user
from app.utils.auth_decorator import acl_required_to_login
from app.utils.validation_decorator import validate_with
from app.schemas.user_schema import UserCreate


# @acl_required_to_login(["ACL_ADMIN"])
@validate_with(UserCreate)
def create_user_main(**kwargs):
    return create_user(**kwargs)
