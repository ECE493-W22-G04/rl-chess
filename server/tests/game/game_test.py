import json
import pytest
from flask import jsonify
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token

from server.api import create_app
from server.api.models import Game, Player, db
from server.tests.constants import TEST_EMAIL, TEST_PASSWORD


@pytest.fixture
def client() -> FlaskClient:
    app = create_app()
    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture
def player(client: FlaskClient):
    player = Player(email=TEST_EMAIL, password=TEST_PASSWORD)
    db.session.add(player)
    db.session.commit()
    yield player


def test_game_jsonify(player: Player):
    game = Game(host_email=player.email)
    resp = jsonify(game.__dict__)
    body = json.loads(resp.data)

    assert 'black_player' in body
    assert 'white_player' in body
    assert 'host' in body
    assert 'id' in body


def test_create_game(client: FlaskClient, player: Player):
    access_token = create_access_token(identity=player.email)
    resp = client.post('/api/games/', headers={'Authorization': f'Bearer {access_token}'})
    assert resp.status_code == 201


def test_create_game_unauthed(client):
    resp = client.post('/api/games/')
    assert resp.status_code == 401
