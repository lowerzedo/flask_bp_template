from app.database.oracle_decorator import with_oracle_connection
from app.models.user_models import create_user_query

@with_oracle_connection
def create_user(user_data: Dict[str, str], *, conn, cursor) -> Dict[str, Any]:
    """
    A service to create a user.

    :param user_data: Dictionary containing user details. (str for key and str for value)
    :param conn: Oracle connection.
    :param cursor: Oracle cursor.
    
    :return: 
        - Dictionary containing the new user ID.
    """
    username = user_data.get('username')
    email = user_data.get('email')
    password = user_data.get('password')  # Note: Hash the password in production!
    user_id = create_user_query(username, email, password, conn=conn, cursor=cursor)
    return {"user_id": user_id}