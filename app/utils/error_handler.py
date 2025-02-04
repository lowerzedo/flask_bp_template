from typing import Tuple, Dict, Any
from flask import jsonify
from werkzeug.exceptions import HTTPException

def handle_error(e: Exception) -> Tuple[Dict[str, Any], int]:
    if isinstance(e, HTTPException):
        return jsonify({
            'error': e.description,
            'status_code': e.code
        }), e.code
    
    return jsonify({
        'error': str(e),
        'status_code': 500
    }), 500