from typing import List, Dict, Any, Optional

def create_user_query(username: str, email: str, password: str, *, conn, cursor) -> int:
    """
    Create a new user in the database.

    :param username: Username of the new user.
    :param email: User's email.
    :param password: Hashed password.
    :param conn: MySQL connection.
    :param cursor: MySQL cursor.
    :return: ID of the newly created user.
    """
    sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
    cursor.execute(sql, (username, email, password))
    return cursor.lastrowid

def get_user_by_id_query(user_id: int, *, conn, cursor) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user by ID.

    :param user_id: ID of the user.
    :param conn: MySQL connection.
    :param cursor: MySQL cursor.
    :return: User record as a dictionary or None if not found.
    """
    sql = "SELECT id, username, email FROM users WHERE id = %s"
    cursor.execute(sql, (user_id,))
    return cursor.fetchone()

def update_user_query(user_id: int, username: str, email: str, *, conn, cursor) -> int:
    """
    Update an existing user.

    :param user_id: ID of the user.
    :param username: New username.
    :param email: New email.
    :param conn: MySQL connection.
    :param cursor: MySQL cursor.
    :return: Number of rows affected.
    """
    sql = "UPDATE users SET username = %s, email = %s WHERE id = %s"
    cursor.execute(sql, (username, email, user_id))
    return cursor.rowcount

def delete_user_query(user_id: int, *, conn, cursor) -> int:
    """
    Delete a user by ID.

    :param user_id: ID of the user.
    :param conn: MySQL connection.
    :param cursor: MySQL cursor.
    :return: Number of rows affected.
    """
    sql = "DELETE FROM users WHERE id = %s"
    cursor.execute(sql, (user_id,))
    return cursor.rowcount

def list_users_query(*, conn, cursor) -> List[Dict[str, Any]]:
    """
    List all users.

    :param conn: MySQL connection.
    :param cursor: MySQL cursor.
    :return: List of user records.
    """
    sql = "SELECT id, username, email FROM users"
    cursor.execute(sql)
    return cursor.fetchall()
