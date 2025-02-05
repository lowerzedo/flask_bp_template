from typing import Dict, TypedDict
from app.models.user_models import create_user_query
from flask import current_app, jsonify, Response
from mysql.connector import MySQLConnection
from app.database.mysql_decorator import conn_msql


class StudentData(TypedDict):
    student_name: str
    student_id: str
    student_course: str

@conn_msql
def create_user(validated_data: StudentData, **kwargs: Dict[str, MySQLConnection]) -> Response:
    """
    Creates a new user in the database with the provided validated data.
    Args:
        validated_data (dict): A dictionary containing the validated user data.
            Expected keys are:
                - "student_name" (str): The name of the student.
                - "student_id" (str): The ID of the student.
                - "student_course" (str): The course of the student.
        **kwargs: Additional keyword arguments. Expected keys are:
            - "msql" (MySQLConnection): The MySQL connection object.
    Returns:
        Response: A Flask response object with a success message and HTTP status code 201.
    """
    student_name = validated_data["student_name"]
    student_id = validated_data["student_id"]
    student_course = validated_data["student_course"]

    current_app.logger.info(f"Creating new user with student ID: {student_id}")

    conn: MySQLConnection = kwargs['msql']
    cursor = conn.cursor()

    query_obj: StudentData = {
        "student_name": student_name,
        "student_id": student_id,
        "student_course": student_course,
    }

    print(f"Creating user with details: {query_obj}")

    try:
        create_user_query(cursor, query_obj)
        conn.commit()
        current_app.logger.info(f"Successfully created user with student ID: {student_id}")
        return jsonify({"message": "User created successfully"}), 201
    finally:
        cursor.close()
