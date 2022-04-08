def test_default_route(client):
    response = client.get("/", follow_redirects=True)
    assert "Hello! I'm a message that came from the backend" in response.json["message"]
