from functools import wraps
from typing import Callable, Any
from flask import request, jsonify

def require_auth(f: Callable) -> Callable:
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'No authorization header'}), 401
            
        try:
            # Here you would implement your token validation logic
            # token = auth_header.split(' ')[1]
            # validate_token(token)
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Invalid token'}), 401
            
    return decorated_function