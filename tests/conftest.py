import pytest
from functools import wraps

# Mock authentication decorator
@pytest.fixture(autouse=True)
def mock_acl_required_to_login(monkeypatch):
    """Mock the ACL authentication decorator to always succeed"""
    
    def fake_decorator(allowed_acl):
        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                # Add fake access list and samaccount to kwargs
                kwargs["accesslist"] = {"ACL": ["TEST_ACL"]}
                kwargs["samaccount"] = "test_user"
                return f(*args, **kwargs)
            return wrapper
        return decorator
    
    # Patch the decorator in the auth_decorator module
    monkeypatch.setattr("app.utils.auth_decorator.acl_required_to_login", fake_decorator)

@pytest.fixture(autouse=True)
def mock_get_secret(monkeypatch):
    """Mock the get_secret function to return test values"""
    
    def fake_get_secret():
        return (
            "fake_msql_acl_conn_string",
            "fake_msql_ei_conn_string", 
            "fake_gims_ro_conn_string",
            "fake_oracle_w_conn_string",
            "fake_microsoft_auth_url",
            "fake_finance_db_conn_string"
        )
    
    monkeypatch.setattr("app.utils.auth_decorator.get_secret", fake_get_secret)
    monkeypatch.setattr("app.utils.secrets.get_secret", fake_get_secret)

@pytest.fixture
def app_with_auth_mocks(monkeypatch):
    """Create a Flask app with authentication mocks for integration tests"""
    from app import create_app
    
    # Create test app
    app = create_app("testing")
    
    # Create a mock version of acl_required_to_login that always passes
    def mock_auth(allowed_acl):
        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                # Add fake access list and samaccount to kwargs
                kwargs["accesslist"] = {"ACL": ["admin", "TEST_ACL"]}
                kwargs["samaccount"] = "test_user"
                return f(*args, **kwargs)
            return wrapper
        return decorator
    
    # Make sure the mock is applied to the correct location
    monkeypatch.setattr("app.utils.auth_decorator.acl_required_to_login", mock_auth)
    monkeypatch.setattr("app.controllers.user_controllers.acl_required_to_login", mock_auth)
    
    return app

@pytest.fixture
def client(app_with_auth_mocks):
    """Create a test client with auth mocks"""
    with app_with_auth_mocks.test_client() as client:
        yield client