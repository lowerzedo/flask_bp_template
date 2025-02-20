from flask_smorest import Blueprint
from app.controllers.user_controllers import create_user_main, get_all_users_main
from app.schemas.user_schema import UserCreateSchema

bp = Blueprint('blueprint', __name__)

@bp.route("/user", methods=["POST"])
@bp.arguments(UserCreateSchema)
@bp.response(201, description="User created successfully")
def create_user_endpoint(new_data):
    return create_user_main(new_data)

@bp.route("/user", methods=["GET"])
def get_all_users_endpoint():
    return get_all_users_main()