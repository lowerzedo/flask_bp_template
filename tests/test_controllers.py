def test_get_users_endpoint(client):
    """Test the get users endpoint with mocked authentication"""
    
    # Make request to protected endpoint
    response = client.get('/api/user')
    
    # Check response
    assert response.status_code == 200
    # Add more assertions based on expected response