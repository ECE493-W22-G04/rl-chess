import json
from flask.testing import FlaskClient


def test_create_game_unauthed(client: FlaskClient):
    resp = client.post('/api/games/', data=json.dumps({'isPvP': False}))
    assert resp.status_code == 401


def test_create_computer_game(client: FlaskClient, access_token: str):
    resp = client.post('/api/games/', data=json.dumps({'isPvP': False}), headers={'Authorization': f'Bearer {access_token}'}, content_type='application/json')
    assert resp.status_code == 201
    resp_json = json.loads(resp.json)
    assert 'id' in resp_json
    assert not resp_json['is_pvp']


def test_create_pvp_game(client: FlaskClient, access_token: str):
    resp = client.post('/api/games/', data=json.dumps({'isPvP': True}), headers={'Authorization': f'Bearer {access_token}'}, content_type='application/json')
    assert resp.status_code == 201
    resp_json = json.loads(resp.json)
    assert 'id' in resp_json
    assert resp_json['is_pvp']


def test_create_pvp_game_missing_player(client: FlaskClient, missing_player_access_token: str):
    resp = client.post('/api/games/', data=json.dumps({'isPvP': True}), headers={'Authorization': f'Bearer {missing_player_access_token}'}, content_type='application/json')
    assert resp.status_code == 400
    resp_json = json.loads(resp.json)
    assert 'err' in resp_json
    assert resp_json['err'] == "Player does not exist"


def test_get_game(client: FlaskClient, access_token: str):
    post_resp = client.post('/api/games/', data=json.dumps({'isPvP': False}), headers={'Authorization': f'Bearer {access_token}'}, content_type='application/json')
    post_resp_json = json.loads(post_resp.json)
    game_id = post_resp_json['id']

    get_resp = client.get(f'/api/games/{game_id}', headers={'Authorization': f'Bearer {access_token}'})
    assert get_resp.status_code == 200

    get_resp_json = json.loads(get_resp.json)
    assert get_resp_json['id'] == game_id
