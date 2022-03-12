import pytest
import sys
import os
import json

# access parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api import create_app


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

def test_valid_signup_signin_route(client):
    email = "test@test.com"
    password = "testpass"
    # Test signup
    response = client.post("/api/auth/signup", follow_redirects=True, 
                       data=json.dumps({"email": email, "password": password}),
                       content_type='application/json')
    assert f"Registration Successful {email}!" in response.json["message"]
    # Test signin
    response = client.post("/api/auth/signin", follow_redirects=True, 
                       data=json.dumps({"email": email, "password": password}),
                       content_type='application/json')
    assert f"Welcome {email}" in response.json["message"]

def test_email_exists_signup_route(client):
    email = "test@test.com"
    password = "testpass"
    # Test signup
    response = client.post("/api/auth/signup", follow_redirects=True, 
                       data=json.dumps({"email": email, "password": password}),
                       content_type='application/json')
    assert f"Registration Successful {email}!" in response.json["message"]
    # Test repeated signup failure
    response = client.post("/api/auth/signup", follow_redirects=True, 
                       data=json.dumps({"email": email, "password": password}),
                       content_type='application/json')
    assert f"Email already exists {email}" in response.json["message"]
    