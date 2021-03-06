import json
from flask_socketio import SocketIO
from flask import Flask
from flask.testing import FlaskClient
from flask_socketio.test_client import SocketIOTestClient
from pytest import fail

from server.api.models import Player


def test_broadcasts_other_player_as_winner_in_pvp(socketio: SocketIO, socketio_client: SocketIOTestClient, client: FlaskClient, access_tokens: str, players: list[Player], app: Flask):
    # This test case covers:
    # FR 28
    # In Partition Tests:
    # works normally

    # Create computer game
    resp = client.post('/api/games/', data=json.dumps({'isPvP': True}), headers={'Authorization': f'Bearer {access_tokens[0]}'}, content_type='application/json')
    assert resp.status_code == 201
    game = resp.json
    game_id = game['id']

    # Create second client
    socketio_client2 = socketio.test_client(app, flask_test_client=client)

    # Join game
    socketio_client.emit('join', {'user': players[0].email, 'gameId': game_id})
    socketio_client2.emit('join', {'user': players[1].email, 'gameId': game_id})

    # Start game
    socketio_client2.emit('pick_side', {'gameId': game_id, 'color': 'white', 'user': players[0].email})

    # Have client2 concede
    socketio_client2.emit('concede', {'gameId': game_id, 'currentPlayer': players[1].email})

    messages1 = socketio_client.get_received()
    messages2 = socketio_client2.get_received()

    # Check the last message sent was a game over message
    for messages in [messages1, messages2]:
        last_message = messages[-1]
        if last_message['name'] != 'game_over':
            fail('Last message was not game over')

        json_message = last_message['args'][0]
        winner = json_message['winner']
        assert winner == players[0].email


def test_broadcasts_other_player_as_winner_in_pvc(socketio_client: SocketIOTestClient, client: FlaskClient, access_token: str, player: Player):
    # This test case covers:
    # FR 28
    # In Partition Tests:
    # works normally

    # Create computer game
    resp = client.post('/api/games/', data=json.dumps({'isPvP': False}), headers={'Authorization': f'Bearer {access_token}'}, content_type='application/json')
    assert resp.status_code == 201
    game = resp.json
    game_id = game['id']

    # Join game
    socketio_client.emit('join', {'user': player.email, 'gameId': game_id})

    # Start game
    socketio_client.emit('pick_side', {'gameId': game_id, 'color': 'white', 'user': player.email})

    # Concede
    socketio_client.emit('concede', {'gameId': game_id, 'currentPlayer': player.email})

    messages = socketio_client.get_received()

    # Check the last message sent was a game over message
    last_message = messages[-1]
    if last_message['name'] != 'game_over':
        fail('Last message was not game over')

    json_message = last_message['args'][0]
    winner = json_message['winner']
    assert winner == 'RL Agent'
