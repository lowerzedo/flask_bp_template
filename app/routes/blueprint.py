from flask import Blueprint
from app.controllers.user_controllers import create_user_main

blueprint = Blueprint('blueprint', __name__)

blueprint.route('/user', methods=['POST'])(create_user_main)