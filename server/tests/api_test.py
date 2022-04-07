import json


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
    assert "This is the homepage of user with token: " + \
        token in response.json["message"]


def test_valid_signup_signin_route(client):
    # This test case covers:
    # FR 3
    # In Partition Tests:
    # works normally
    email = "test@test.com"
    password = "testpass"
    # Test signup
    response = client.post("/api/auth/signup", follow_redirects=True, data=json.dumps({"email": email, "password": password}), content_type='application/json')
    assert f"Registration Successful {email}!" in response.json["message"]
    # Test signin
    response = client.post("/api/auth/signin", follow_redirects=True, data=json.dumps({"email": email, "password": password}), content_type='application/json')
    assert f"Welcome {email}" in response.json["message"]


def test_email_exists_signup_route(client):
    # This test case covers:
    # FR 1
    # In Partition Tests:
    # works normally
    # Out of Partition tests:
    # user exists
    email = "test@test.com"
    password = "testpass"
    # Test signup
    response = client.post("/api/auth/signup", follow_redirects=True, data=json.dumps({"email": email, "password": password}), content_type='application/json')
    assert f"Registration Successful {email}!" in response.json["message"]
    # Test repeated signup failure
    response = client.post("/api/auth/signup", follow_redirects=True, data=json.dumps({"email": email, "password": password}), content_type='application/json')
    assert f"Email already exists {email}" in response.json["message"]


def test_invalid_email_format_signup(client):
    # This test case covers:
    # FR 1
    # Out of Partition tests:
    # invalid email
    # no email
    email = "thisisnotanemail"
    password = "testpass"
    # Test signup with invalid email
    response = client.post("/api/auth/signup", follow_redirects=True, data=json.dumps({"email": email, "password": password}), content_type='application/json')
    assert "Inavlid email format" in response.json["message"]
    # Test signup without email
    response = client.post("/api/auth/signup", follow_redirects=True, data=json.dumps({"email": "", "password": password}), content_type='application/json')
    assert "No email provided!" in response.json["message"]


def test_invalid_password_signup(client):
    # This test case covers:
    # FR 1
    # Out of Partition tests:
    # 7 character pass
    # no pass
    email = "test@test.com"
    password = "1234567"
    # Test signup with invalid password
    response = client.post("/api/auth/signup", follow_redirects=True, data=json.dumps({"email": email, "password": password}), content_type='application/json')
    assert "password must be 8 characters or more" in response.json["message"]
    # Test signup with no password
    response = client.post("/api/auth/signup", follow_redirects=True, data=json.dumps({"email": email, "password": ""}), content_type='application/json')
    assert "No password provided" in response.json["message"]
