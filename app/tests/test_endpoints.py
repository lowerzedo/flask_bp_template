import unittest
from flask import current_app
from app import create_app
from unittest.mock import patch, MagicMock


class TestEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch("app.utils.secrets.get_secret")
    @patch("app.utils.auth_decorator.requests.get")
    def test_protected_endpoint_with_microsoft_auth(
        self, mock_auth_request, mock_get_secret
    ):
        # Mock the authentication response
        mock_auth_response = MagicMock()
        mock_auth_response.status_code = 200
        mock_auth_response.text = '{"msg": {"onPremisesSamAccountName": "test_user", "groups": ["admin_group"]}}'
        mock_auth_request.return_value = mock_auth_response

        # Mock secrets
        mock_get_secret.return_value = ["mysql_creds", "mssql_creds", "oracle_creds"]

        # Test the endpoint
        headers = {"Authorization": "Bearer test_token"}
        response = self.client.get("/your-endpoint", headers=headers)

        self.assertEqual(response.status_code, 200)

    @patch("app.utils.secrets.get_secret")
    @patch("app.utils.auth_decorator.requests.get")
    def test_protected_endpoint_with_cas_auth(self, mock_auth_request, mock_get_secret):
        # Mock CAS validation response
        mock_auth_response = MagicMock()
        mock_auth_response.status_code = 200
        mock_auth_response.json.return_value = {
            "serviceResponse": {
                "authenticationSuccess": {
                    "attributes": {"memberOf": ["test_group"], "username": "test_user"}
                }
            }
        }
        mock_auth_request.return_value = mock_auth_response

        # Mock secrets
        mock_get_secret.return_value = ["mysql_creds", "mssql_creds", "oracle_creds"]

        # Test the endpoint with CAS ticket
        response = self.client.get("/your-endpoint?ticket=test_ticket")

        self.assertEqual(response.status_code, 200)

    def test_unauthorized_access(self):
        # Test endpoint without authentication
        response = self.client.get("/your-endpoint")
        self.assertEqual(response.status_code, 401)

    @patch("app.utils.validation_decorator.request")
    def test_endpoint_with_validation(self, mock_request):
        # Mock request data
        mock_request.json = {"field1": "value1", "field2": "value2"}

        # Test endpoint with validation
        response = self.client.post("/user", json=mock_request.json)

        self.assertEqual(response.status_code, 200)
