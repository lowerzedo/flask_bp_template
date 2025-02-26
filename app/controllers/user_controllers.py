from app.services.user_services import create_user, get_all_users
from app.utils.auth_decorator import acl_required_to_login

@acl_required_to_login(['admin'])
def create_user_main(new_data):
    """
    Create a new user and return success.
    new_data: dict - validated data from request payload.
    """
    return create_user(new_data)


@acl_required_to_login(['admin'])
def get_all_users_main():
    return get_all_users()
