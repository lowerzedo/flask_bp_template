from flask import Blueprint, request, jsonify
from app.controllers.user_controller import UserController

user_bp = Blueprint('user', __name__)
user_controller = UserController()

@user_bp.route('/users', methods=['POST'])
def create_user():
    response, status_code = user_controller.create_user(request.json)
    return jsonify(response), status_code

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id: int):
    response, status_code = user_controller.get_user(user_id)
    return jsonify(response), status_code

@user_bp.route('/users', methods=['GET'])
def get_users():
    response, status_code = user_controller.get_users()
    return jsonify(response), status_code