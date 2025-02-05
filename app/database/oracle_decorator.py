import cx_Oracle
from functools import wraps
from app.utils.secrets import get_secret
from flask import current_app

def conn(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            oracle_w = get_secret()[2].split(':')
            dsn_tns = cx_Oracle.makedsn(oracle_w[0], oracle_w[1], oracle_w[2])
            conn = cx_Oracle.connect(oracle_w[3], oracle_w[4], dsn=dsn_tns,
                                     encoding="UTF-8", nencoding="UTF-8")
            kwargs['con'] = conn
            result = fn(*args, **kwargs)
            conn.commit()  # Optionally commit at this level if appropriate.
            return result
        except Exception as e:
            current_app.logger.exception(f"Oracle error: {str(e)}")
            if 'conn' in locals():
                conn.rollback()
            raise e
        finally:
            if 'conn' in locals():
                conn.close()
    return wrapper


def conn_execute(stats):
    def decorator(fn):
        @wraps(fn)
        def wrapper(cursor, query_obj):
            query = fn(cursor, query_obj)
            try:
                res = cursor.execute(query, query_obj)
                if stats == 'GET':
                    columns = [col[0] for col in cursor.description]
                    return [dict(zip(columns, row)) for row in cursor.fetchall()]
                else:
                    return res
            except Exception as e:
                
                raise e
        return wrapper
    return decorator