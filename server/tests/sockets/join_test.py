import json
from flask.testing import FlaskClient
from flask_socketio.test_client import SocketIOTestClient
from pytest import fail

from ..constants import TEST_EMAIL


def test_join_pvc(socketio_client: SocketIOTestClient, client: FlaskClient, access_token: str):
    # This test case covers:
    # FR 13
    # In Partition Tests:
    # works normally

    # Create computer game
    resp = client.post('/api/games/', data=json.dumps({'isPvP': False}), headers={'Authorization': f'Bearer {access_token}'}, content_type='application/json')
    assert resp.status_code == 201
    game = resp.json
    game_id = game['id']

    socketio_client.emit('join', {'user': TEST_EMAIL, 'gameId': game_id})

    messages = socketio_client.get_received()
    for message in messages:
        if message['name'] == 'room_full':
            return
    fail('Did not find room_full message after joining computer room')
