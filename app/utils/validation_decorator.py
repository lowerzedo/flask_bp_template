from functools import wraps
from flask import request, jsonify, Response
from marshmallow import Schema, ValidationError

from typing import Type, Callable, TypeVar, cast, Any



T = TypeVar('T', bound=Schema)
F = TypeVar('F', bound=Callable[..., Response])

def validate_with(schema_class: Type[T]) -> Callable[[F], F]:
    """
    A decorator that validates the incoming JSON request data against a given Marshmallow schema.
    Args:
        schema_class (Type[T]): The Marshmallow schema class to validate the request data against.
    Returns:
        Callable[[F], F]: A decorator function that wraps the original function with validation logic.
    The decorator function:
        - Instantiates the schema class.
        - Attempts to load and validate the incoming JSON data from the request.
        - If validation is successful, it calls the original function with the validated data added to the keyword arguments.
        - If validation fails, it returns a JSON response with an error message and a 400 status code.
    """
    def decorator(f: F) -> F:
        @wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Response:
            schema = schema_class()
            try:
                validated_data = schema.load(request.json)
                return f(*args, **{**kwargs, "validated_data": validated_data})
            except ValidationError as e:
                return jsonify({"error": "Validation failed", "messages": e.messages}), 400
        return cast(F, wrapper)
    return decorator
