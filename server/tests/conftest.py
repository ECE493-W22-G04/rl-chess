import pytest
from flask_socketio import SocketIO
from server import create_app
from .fixtures.player import player, access_token


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    SocketIO(app)

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
