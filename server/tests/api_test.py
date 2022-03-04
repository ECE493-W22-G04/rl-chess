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
    test = client.get("/", follow_redirects=True)
    assert b"This is the default route for this app, you can write more routes here" in test.data
