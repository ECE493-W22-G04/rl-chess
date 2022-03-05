import pytest
import sys
import os

# access parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import create_app


# Preload an app client which we can access in the tests
@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


def test_default_route(client):
    response = client.get("/", follow_redirects=True)
    assert "Hello! I'm a message that came from the backend" in response.json["message"]

def test_home_route(client):
    response = client.get("/api/home", follow_redirects=True)
    assert "This is the generic homepage" in response.json["message"]

def test_invalid_token_user_route(client):
    response = client.get("/api/user", follow_redirects=True)
    assert "token given in authorization header is invalid" in response.json["message"]

def test_valid_token_user_route(client):
    token = "1"
    response = client.get("/api/user", follow_redirects=True, headers={"Authorization": token})
    assert "This is the homepage of user with token: " + token in response.json["message"]
    
