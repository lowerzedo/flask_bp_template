import pymssql
from functools import wraps
from typing import Callable, Any
from flask import current_app


def with_mssql_connection(func: Callable) -> Callable:
    """
    Decorator to provide an MSSQL connection to the decorated function.

    :param func: Function to wrap.
    :return: Wrapped function with MSSQL connection and cursor.
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        conn = None
        cursor = None
        try:
            conn = pymssql.connect(
                server=current_app.config.get("MSSQL_SERVER", "localhost"),
                user=current_app.config.get("MSSQL_USER", "user"),
                password=current_app.config.get("MSSQL_PASSWORD", "password"),
                database=current_app.config.get("MSSQL_DB", "database"),
            )
            cursor = conn.cursor(as_dict=True)
            kwargs["conn"] = conn
            kwargs["cursor"] = cursor
            result = func(*args, **kwargs)
            conn.commit()
            return result
        except pymssql.Error as e:
            if conn:
                conn.rollback()
            raise Exception(f"MSSQL error: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return wrapper
