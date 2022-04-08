import json
from flask_socketio import SocketIO
from flask import Flask
from flask.testing import FlaskClient
from flask_socketio.test_client import SocketIOTestClient
from pytest import fail

from server.api.models import Player


def test_draw_pvp(socketio: SocketIO, socketio_client: SocketIOTestClient, client: FlaskClient, access_tokens: str, players: list[Player], app: Flask):
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

    # Have client1 offer draw
    socketio_client.emit('offer_draw', {'gameId': game_id, 'currentPlayer': players[0].email})

    # Have client12 accept the offer
    socketio_client.emit('accept_draw', {'gameId': game_id})

    messages1 = socketio_client.get_received()
    messages2 = socketio_client2.get_received()

    # Check the last message sent was a game over message
    for messages in [messages1, messages2]:
        last_message = messages[-1]
        if last_message['name'] != 'game_over':
            fail('Last message was not game over')

        json_message = json.loads(last_message['args'][0])
        winner = json_message['winner']
        assert winner == 'Nobody'
