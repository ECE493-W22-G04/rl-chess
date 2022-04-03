import json
from flask import Flask
import pytest
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token

from server.api.models import Player, db
from ..constants import TEST_EMAIL, TEST_PASSWORD


@pytest.fixture
def player(app: Flask) -> Player:
    with app.app_context():
        player = Player(email=TEST_EMAIL, password=TEST_PASSWORD)
        db.session.add(player)
        db.session.commit()

        yield player


@pytest.fixture
def access_token(player: Player) -> str:
    yield create_access_token(identity=player.email)


def test_create_game_unauthed(client: FlaskClient):
    resp = client.post('/api/games/', data=json.dumps({'isPvP': False}))
    assert resp.status_code == 401


# TODO: Fix these tests
# def test_create_computer_game(client: FlaskClient, access_token: str):
#     resp = client.post('/api/games/', data=json.dumps({'isPvP': False}), headers={'Authorization': f'Bearer {access_token}'})
#     assert resp.status_code == 201
#     assert 'id' in resp.json
#     assert not resp.json['is_pvp']

# def test_create_pvp_game(client: FlaskClient, access_token: str):
#     resp = client.post('/api/games/', data=json.dumps({'isPvP': True}), headers={'Authorization': f'Bearer {access_token}'})
#     assert resp.status_code == 201
#     assert 'id' in resp.json
#     assert resp.json['is_pvp']

# def test_get_game(client: FlaskClient, access_token: str):
#     resp = client.post('/api/games/', data=json.dumps({'isPvP': False}), headers={'Authorization': f'Bearer {access_token}'})
#     game_id = resp.json['id']

#     resp = client.get(f'/api/games/{game_id}', headers={'Authorization': f'Bearer {access_token}'})
#     assert resp.status_code == 200
#     assert resp.json['id'] == game_id
