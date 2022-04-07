from flask import Flask
import pytest
from flask_socketio import SocketIO
from flask_socketio.test_client import SocketIOTestClient
from server import create_app
from .fixtures.player import player, access_token


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def socketio_client(app: Flask) -> SocketIOTestClient:
    socketio = SocketIO(app)
    return socketio.test_client(app)


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
