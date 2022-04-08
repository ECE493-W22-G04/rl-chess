import pytest
from flask import Flask
from flask.testing import FlaskClient
from flask_socketio import SocketIO
from flask_socketio.test_client import SocketIOTestClient
from server import create_app
from server.ws.socket_events import register_ws_events
from .fixtures.player import player, missing_player, players, access_token, access_tokens, missing_player_access_token
from server.api.models import db


@pytest.fixture()
def app() -> Flask:
    app = create_app()
    app.config.update({"TESTING": True, "SQLALCHEMY_DATABASE_URI": f'sqlite:///:memory:'})

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app) -> FlaskClient:
    return app.test_client()


@pytest.fixture()
def socketio(app: Flask) -> SocketIOTestClient:
    socketio = SocketIO(app)
    register_ws_events(socketio)
    yield socketio


@pytest.fixture()
def socketio_client(socketio: SocketIO, app: Flask, client: FlaskClient) -> SocketIOTestClient:
    return socketio.test_client(app, flask_test_client=client)


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
