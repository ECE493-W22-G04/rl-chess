import json
from flask_socketio import SocketIO
from flask import Flask
from flask.testing import FlaskClient
from flask_socketio.test_client import SocketIOTestClient

from server.api.models import Player


def test_broadcasts_game_has_started_in_pvp(socketio: SocketIO, socketio_client: SocketIOTestClient, client: FlaskClient, access_tokens: list[str], players: list[Player], app: Flask):
    # Create computer game
    resp = client.post('/api/games/', data=json.dumps({'isPvP': True}), headers={'Authorization': f'Bearer {access_tokens[0]}'}, content_type='application/json')
    assert resp.status_code == 201
    game = json.loads(resp.json)
    game_id = game['id']

    # Create second client
    socketio_client2 = socketio.test_client(app, flask_test_client=client)

    # Join game
    socketio_client.emit('join', {'user': players[0].email, 'gameId': game_id})
    socketio_client2.emit('join', {'user': players[1].email, 'gameId': game_id})

    # Start game
    socketio_client2.emit('pick_side', {'gameId': game_id, 'color': 'white', 'user': players[0].email})

    messages1 = socketio_client.get_received()
    messages2 = socketio_client2.get_received()

    # See if each client receives game started signal
    for messages in [messages1, messages2]:
        game_start_message_count = 0
        for message in messages:
            if message['name'] != 'update':
                continue
            json_body = json.loads(message['args'][0])
            if json_body['has_started'] == False:
                continue
            game_start_message_count += 1
            break
        assert game_start_message_count == 1


def test_broadcasts_game_has_started_in_pvc(socketio_client: SocketIOTestClient, client: FlaskClient, access_token: str, player: list[Player], app: Flask):
    # Create computer game
    resp = client.post('/api/games/', data=json.dumps({'isPvP': False}), headers={'Authorization': f'Bearer {access_token}'}, content_type='application/json')
    assert resp.status_code == 201
    game = json.loads(resp.json)
    game_id = game['id']

    # Join game
    socketio_client.emit('join', {'user': player.email, 'gameId': game_id})

    # Start game
    socketio_client.emit('pick_side', {'gameId': game_id, 'color': 'white', 'user': player.email})
    
    messages = socketio_client.get_received()

    # See if each client receives game started signal
    game_start_message_count = 0
    for message in messages:
        if message['name'] != 'update':
            continue
        json_body = json.loads(message['args'][0])
        if json_body['has_started'] == False:
            continue
        game_start_message_count += 1
        break
    assert game_start_message_count == 1
