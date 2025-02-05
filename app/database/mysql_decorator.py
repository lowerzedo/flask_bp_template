import mysql.connector
from app.utils.secrets import get_secret


def conn_msql(fn):
    """
    Decorator to handle MySQL connection and closing.
    """
    def wrapper(*args, **kwargs):
        db_mysql = get_secret()[1].split(':')
        conn = mysql.connector.connect(user=db_mysql[0], password=db_mysql[1],host=db_mysql[2], database=db_mysql[3])
        kwargs['msql'] = conn
        resp = fn(*args, **kwargs)
        conn.close()
        return resp
    return wrapper


def conn_execute_msql(stats):
    """
    Decorator to handle MySQL query execution with different operation types.
    stats: 'GET' for select operations, anything else for other operations
    """
    def decorator(fn):
        def wrapper(cursor,query_obj):
            query = fn(cursor, query_obj)
            res = cursor.execute(query, query_obj)
            return [dict(zip([x[0] for x in cursor.description], row)) for row in cursor.fetchall()] if stats=='GET' else res
        return wrapper
    return decorator

