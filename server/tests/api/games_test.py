import json
from flask.testing import FlaskClient


def test_create_game_unauthed(client: FlaskClient):
    # This test case covers:
    # FR 10
    # In Partition Tests:
    # works normally
    # Out of Partition tests:
    # user is unauthenticated
    resp = client.post('/api/games/', data=json.dumps({'isPvP': False}))
    assert resp.status_code == 401


def test_create_computer_game(client: FlaskClient, access_token: str):
    # This test case covers:
    # FR 6
    # FR 10
    # In Partition Tests:
    # works normally
    resp = client.post('/api/games/', data=json.dumps({'isPvP': False}), headers={'Authorization': f'Bearer {access_token}'}, content_type='application/json')
    assert resp.status_code == 201
    assert 'id' in resp.json
    assert not resp.json['is_pvp']


def test_create_pvp_game(client: FlaskClient, access_token: str):
    # This test case covers:
    # FR 10
    # In Partition Tests:
    # works normally
    resp = client.post('/api/games/', data=json.dumps({'isPvP': True}), headers={'Authorization': f'Bearer {access_token}'}, content_type='application/json')
    assert resp.status_code == 201

    assert 'id' in resp.json
    assert resp.json['is_pvp']


def test_create_pvp_game_missing_player(client: FlaskClient, missing_player_access_token: str):
    # This test case covers:
    # FR 10
    # In Partition Tests:
    # works normally
    # Out of Partition tests:
    # user is unauthenticated
    resp = client.post('/api/games/', data=json.dumps({'isPvP': True}), headers={'Authorization': f'Bearer {missing_player_access_token}'}, content_type='application/json')
    assert resp.status_code == 400
    assert 'err' in resp.json

    assert resp.json['err'] == "Player does not exist"


def test_get_game(client: FlaskClient, access_token: str):
    # This test case covers:
    # FR 11
    # In Partition Tests:
    # works normally
    post_resp = client.post('/api/games/', data=json.dumps({'isPvP': False}), headers={'Authorization': f'Bearer {access_token}'}, content_type='application/json')
    game_id = post_resp.json['id']

    get_resp = client.get(f'/api/games/{game_id}', headers={'Authorization': f'Bearer {access_token}'})
    assert get_resp.status_code == 200

    assert get_resp.json['id'] == game_id
