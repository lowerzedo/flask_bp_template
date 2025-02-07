from functools import wraps
from flask import request, jsonify, Response
from pydantic import BaseModel, ValidationError
from typing import Type, Callable, TypeVar, cast, Any

T = TypeVar("T", bound=BaseModel)
F = TypeVar("F", bound=Callable[..., Response])


def validate_with(model_class: Type[T]) -> Callable[[F], F]:
    """
    A decorator that validates the incoming JSON request data against a given Pydantic model.
    Args:
        model_class (Type[T]): The Pydantic model class to validate the request data against.
    Returns:
        Callable[[F], F]: A decorator function that wraps the original function with validation logic.
    """

    def decorator(f: F) -> F:
        @wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Response:
            try:
                validated_data = model_class.model_validate(request.json)
                return f(
                    *args, **{**kwargs, "validated_data": validated_data.model_dump()}
                )
            except ValidationError as e:
                return (
                    jsonify({"error": "Validation failed", "messages": e.errors()}),
                    400,
                )

        return cast(F, wrapper)

    return decorator
