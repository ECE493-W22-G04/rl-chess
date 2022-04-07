from flask import Flask
import pytest
from flask_socketio import SocketIO
from flask_socketio.test_client import SocketIOTestClient
from server import create_app
from .fixtures.player import player, access_token
from server.api.models import db


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({"TESTING": True, "SQLALCHEMY_DATABASE_URI": f'sqlite:///:memory:'})

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


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
