import pytest
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token

from server.api import create_app
from server.api.models import Player, db
from server.tests.constants import TEST_EMAIL, TEST_PASSWORD


@pytest.fixture(scope='module')
def client() -> FlaskClient:
    app = create_app()
    with app.test_client() as client:
        yield client


@pytest.fixture(scope='module')
def player() -> Player:
    player = Player(email=TEST_EMAIL, password=TEST_PASSWORD)
    db.session.add(player)
    db.session.commit()

    return player


@pytest.fixture(scope='module')
def access_token(player: Player) -> str:
    yield create_access_token(identity=player.email)


def test_create_game_unauthed(client: FlaskClient):
    resp = client.post('/api/games/')
    assert resp.status_code == 401


def test_create_game(client: FlaskClient, access_token: str):
    resp = client.post('/api/games/', headers={'Authorization': f'Bearer {access_token}'})
    assert resp.status_code == 201
    assert 'id' in resp.json


def test_get_game(client: FlaskClient, access_token: str):
    resp = client.post('/api/games/', headers={'Authorization': f'Bearer {access_token}'})
    game_id = resp.json['id']

    resp = client.get(f'/api/games/{game_id}', headers={'Authorization': f'Bearer {access_token}'})
    assert resp.status_code == 200
    assert resp.json['id'] == game_id
