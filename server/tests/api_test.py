import json


def test_default_route(client):
    response = client.get("/", follow_redirects=True)
    assert "Hello! I'm a message that came from the backend" in response.json["message"]


def test_valid_signup_signin_route(client):
    email = "test@test.com"
    password = "testpass"
    # Test signup
    response = client.post("/api/auth/signup", follow_redirects=True, data=json.dumps({"email": email, "password": password}), content_type='application/json')
    assert f"Registration Successful {email}!" in response.json["message"]
    # Test signin
    response = client.post("/api/auth/signin", follow_redirects=True, data=json.dumps({"email": email, "password": password}), content_type='application/json')
    assert f"Welcome {email}" in response.json["message"]


def test_email_exists_signup_route(client):
    email = "test@test.com"
    password = "testpass"
    # Test signup
    response = client.post("/api/auth/signup", follow_redirects=True, data=json.dumps({"email": email, "password": password}), content_type='application/json')
    assert f"Registration Successful {email}!" in response.json["message"]
    # Test repeated signup failure
    response = client.post("/api/auth/signup", follow_redirects=True, data=json.dumps({"email": email, "password": password}), content_type='application/json')
    assert f"Email already exists {email}" in response.json["message"]
