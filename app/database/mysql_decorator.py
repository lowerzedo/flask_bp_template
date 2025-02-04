import mysql.connector
from functools import wraps
from typing import Callable, Any
from flask import current_app

def with_mysql_connection(func: Callable) -> Callable:
    """
    Decorator to provide a MySQL connection to the decorated function.

    :param func: Function to wrap.
    :return: Wrapped function with MySQL connection and cursor.
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        conn = None
        cursor = None
        try:
            config = {
                'host': current_app.config['MYSQL_HOST'],
                'user': current_app.config['MYSQL_USER'],
                'password': current_app.config['MYSQL_PASSWORD'],
                'database': current_app.config['MYSQL_DB']
            }
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor(dictionary=True)
            kwargs['conn'] = conn
            kwargs['cursor'] = cursor
            result = func(*args, **kwargs)
            conn.commit()
            return result
        except mysql.connector.Error as e:
            if conn:
                conn.rollback()
            raise Exception(f"MySQL error: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    return wrapper
