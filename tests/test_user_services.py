import json
import pytest
from unittest.mock import MagicMock
from flask import Flask, current_app
from app.services.user_services import create_user, get_all_users

class DummyCursor:
    def __init__(self):
        self.closed = False

    def close(self):
        self.closed = True

@pytest.fixture
def dummy_msql():
    # Create a fake MySQL connection and cursor
    dummy_cursor = DummyCursor()
    dummy_conn = MagicMock()
    dummy_conn.cursor.return_value = dummy_cursor
    return dummy_conn

# Override mysql.connector.connect to return our dummy_msql fixture
@pytest.fixture(autouse=True)
def override_mysql_connect(monkeypatch, dummy_msql):
    from mysql import connector
    monkeypatch.setattr(connector, "connect", lambda *args, **kwargs: dummy_msql)

@pytest.fixture
def sample_validated_data():
    return {
        "student_name": "John Doe",
        "student_id": "12345",
        "student_course": "Computer Science"
    }

@pytest.fixture
def fake_create_user_query(monkeypatch):
    # Create a fake create_user_query that does nothing
    mock_query = MagicMock()
    monkeypatch.setattr("app.services.user_services.create_user_query", mock_query)
    return mock_query

@pytest.fixture
def app_context():
    # Create a minimal Flask application context to allow use of current_app
    app = Flask(__name__)
    # Configure a dummy logger
    app.logger = MagicMock()
    with app.test_request_context():
        yield

def test_create_user_success(app_context, dummy_msql, sample_validated_data, fake_create_user_query):
    # Call the create_user function with the sample data and dummy MySQL connection.
    response, status_code = create_user(sample_validated_data, msql=dummy_msql)

    # Check that create_user_query was called with a cursor and the expected query object
    expected_query_obj = {
        "student_name": sample_validated_data["student_name"],
        "student_id": sample_validated_data["student_id"],
        "student_course": sample_validated_data["student_course"],
    }
    fake_create_user_query.assert_called_once()
    args, _ = fake_create_user_query.call_args
    # The first argument should be the dummy cursor
    assert args[0] == dummy_msql.cursor.return_value
    # And the second argument should be the query object as expected
    assert args[1] == expected_query_obj

    # Verify commit was called on the dummy connection
    dummy_msql.commit.assert_called_once()

    # Check that the dummy cursor was closed
    cursor = dummy_msql.cursor.return_value
    assert cursor.closed is True

    # Test the response content and status code
    response_data = json.loads(response.get_data(as_text=True))
    assert response_data == {"message": "User created successfully"}
    assert status_code == 201


def test_get_all_users_success(app_context, dummy_msql):
    # Expected list of users returned from the database
    expected_users = [
        {"student_name": "Alice", "student_id": "1", "student_course": "Math"}
    ]
    # Get the dummy cursor instance and patch fetchall to return our expected data.
    dummy_cursor = dummy_msql.cursor.return_value
    dummy_cursor.fetchall = MagicMock(return_value=expected_users)
    # Ensure that execute is a MagicMock so we can assert its call
    dummy_cursor.execute = MagicMock()

    from app.services.user_services import get_all_users
    # Call get_all_users with the dummy MySQL connection.
    response = get_all_users(msql=dummy_msql)

    # Verify that the SQL query was executed
    dummy_cursor.execute.assert_called_once_with("SELECT * FROM sample_students")
    # Check that the dummy cursor was closed after fetching users
    assert dummy_cursor.closed is True

    # Convert the response to JSON and assert it matches our expected users list.
    response_data = json.loads(response.get_data(as_text=True))
    assert response_data == expected_users