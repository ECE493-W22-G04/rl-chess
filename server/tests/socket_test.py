from flask_socketio import SocketIO
from flask import Flask
import pytest
from flask.testing import FlaskClient
from flask_socketio import SocketIOTestClient

from ..api import create_app

from ..main import socketio


@pytest.fixture
def app() -> Flask:
    app = create_app()
    SocketIO(app, cors_allowed_origins="*")
    app.app_context().push()
    return app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    with app.test_client() as client:
        yield client


@pytest.fixture
def socket_client(app: Flask, client: FlaskClient) -> SocketIOTestClient:
    return socketio.test_client(app, flask_test_client=client)


def test_socket_connection(socket_client: SocketIOTestClient):
    mock_sid = socket_client.socketio.server.manager.sid_from_eio_sid(socket_client.eio_sid, '/')
    assert mock_sid != None
    assert socket_client.is_connected()
