import pytest
from flask_socketio import SocketIO
from server.api import create_app
from .fixtures.player import player, access_token
from server.api.models import db


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({"TESTING": True, "SQLALCHEMY_DATABASE_URI": f'sqlite:///:memory:'})

    SocketIO(app)

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
def runner(app):
    return app.test_cli_runner()
