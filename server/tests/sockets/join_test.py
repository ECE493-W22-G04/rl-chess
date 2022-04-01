from unittest.mock import patch
import pytest
from flask import Flask
from flask.testing import FlaskClient
from flask_socketio import SocketIO
from flask_socketio.test_client import SocketIOTestClient

from ...api.models import Game, Player, db
from ...main import socketio, create_app
from ..constants import TEST_EMAIL, TEST_GAME_ID, TEST_PASSWORD


@pytest.fixture(scope='module')
def app() -> Flask:
    app = create_app()
    SocketIO(app)
    return app


@pytest.fixture(scope='module')
def client(app: Flask) -> FlaskClient:
    with app.test_client() as client:
        yield client


@pytest.fixture(scope='module')
def socketio_client(app: Flask, client: FlaskClient) -> SocketIOTestClient:
    return socketio.test_client(app, '/', flask_test_client=client)


@pytest.fixture(scope='module')
def player(app: Flask) -> Player:
    with app.app_context():
        player = Player(email=TEST_EMAIL, password=TEST_PASSWORD)
        db.session.add(player)
        db.session.commit()
        yield player


@pytest.fixture(scope='module')
def game(app: Flask, player: Player) -> Game:
    with app.app_context():
        yield Game(TEST_EMAIL, is_pvp=False)


def test_join_pvc(socketio_client: SocketIOTestClient, game: Game):
    with patch('flask_socketio.join_room'):
        with patch.dict('server.api.routes.games.current_games', {TEST_GAME_ID: game}):
            try:
                socketio_client.emit('join', {'user': TEST_EMAIL, 'gameId': TEST_GAME_ID})
            except ValueError as err:
                # TODO: Figure out if we can mock join_room
                # join_room will raise this error because SocketIOTestClient does not support joining rooms
                assert err != None
                return

            # Exception from join_room should have been raised
            assert False
