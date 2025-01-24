from typing import Tuple, List, Dict, Any
from flask import jsonify
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserResponse
from app.helpers.db_decorator import with_db_connection
from app.helpers.auth_decorator import require_auth

class UserController:
    def __init__(self):
        self.user_service = UserService()

    @with_db_connection
    @require_auth
    def create_user(self, data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        user_data = UserCreate(**data)
        user = self.user_service.create_user(
            username=user_data.username,
            email=user_data.email
        )
        return UserResponse(**user.__dict__).dict(), 201

    @with_db_connection
    @require_auth
    def get_user(self, user_id: int) -> Tuple[Dict[str, Any], int]:
        user = self.user_service.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return UserResponse(**user.__dict__).dict(), 200

    @with_db_connection
    @require_auth
    def get_users(self) -> Tuple[List[Dict[str, Any]], int]:
        users = self.user_service.get_users()
        return [UserResponse(**user.__dict__).dict() for user in users], 200