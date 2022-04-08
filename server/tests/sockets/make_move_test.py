import json
from flask_socketio import SocketIO
from flask import Flask
from flask.testing import FlaskClient
from flask_socketio.test_client import SocketIOTestClient

from server.api.models import Player


def test_broadcast_move_in_pvp(socketio: SocketIO, socketio_client: SocketIOTestClient, client: FlaskClient, access_tokens: str, players: list[Player], app: Flask):
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

    # Pick side
    socketio_client2.emit('pick_side', {'gameId': game_id, 'color': 'white', 'user': players[0].email})

    # Make move
    valid_first_move = '5,6->5,4'
    socketio_client.emit('make_move', {'gameId': game_id, 'moveStr': valid_first_move, 'promotion': '0'})

    messages1 = socketio_client.get_received()
    messages2 = socketio_client2.get_received()

    # Check whether move is broadcasted to each client
    for messages in [messages1, messages2]:
        move_found = False
        for message in messages:
            if message['name'] != 'update':
                continue
            json_message = message['args'][0]
            board = json_message['board']
            moves = board['moves']
            if len(moves) == 0:
                continue
            for move in moves:
                if move != [[5, 6], [5, 4], None]:
                    continue
                move_found = True
        assert move_found


def test_broadcast_move_in_pvc(socketio_client: SocketIOTestClient, client: FlaskClient, access_token: str, player: Player):
    # Create computer game
    resp = client.post('/api/games/', data=json.dumps({'isPvP': False}), headers={'Authorization': f'Bearer {access_token}'}, content_type='application/json')
    assert resp.status_code == 201
    game = resp.json
    game_id = game['id']

    # Join game
    socketio_client.emit('join', {'user': player.email, 'gameId': game_id})

    # Pick side
    socketio_client.emit('pick_side', {'gameId': game_id, 'color': 'white', 'user': player.email})

    # Make move
    valid_first_move = '5,6->5,4'
    socketio_client.emit('make_move', {'gameId': game_id, 'moveStr': valid_first_move, 'promotion': '0'})

    messages = socketio_client.get_received()

    # Check whether move is broadcasted back
    move_found = False
    for message in messages:
        if message['name'] != 'update':
            continue
        json_message = message['args'][0]
        board = json_message['board']
        moves = board['moves']
        if len(moves) == 0:
            continue
        for move in moves:
            if move != [[5, 6], [5, 4], None]:
                continue
            move_found = True
    assert move_found


def test_computer_makes_move_in_pvc(socketio_client: SocketIOTestClient, client: FlaskClient, access_token: str, player: Player):
    # Create computer game
    resp = client.post('/api/games/', data=json.dumps({'isPvP': False}), headers={'Authorization': f'Bearer {access_token}'}, content_type='application/json')
    assert resp.status_code == 201
    game = resp.json
    game_id = game['id']

    # Join game
    socketio_client.emit('join', {'user': player.email, 'gameId': game_id})

    # Pick side
    socketio_client.emit('pick_side', {'gameId': game_id, 'color': 'white', 'user': player.email})

    # Make move
    valid_first_move = '5,6->5,4'
    socketio_client.emit('make_move', {'gameId': game_id, 'moveStr': valid_first_move, 'promotion': '0'})

    messages = socketio_client.get_received()

    # Check whether computer registers its own move
    last_update = list(filter(lambda message: message['name'] == 'update', messages))[-1]
    last_update_json_message = last_update['args'][0]
    assert len(last_update_json_message['board']['moves']) > 1


def test_computer_makes_first_move_in_pvc(socketio_client: SocketIOTestClient, client: FlaskClient, access_token: str, player: Player):
    # Create computer game
    resp = client.post('/api/games/', data=json.dumps({'isPvP': False}), headers={'Authorization': f'Bearer {access_token}'}, content_type='application/json')
    assert resp.status_code == 201
    game = resp.json
    game_id = game['id']

    # Join game
    socketio_client.emit('join', {'user': player.email, 'gameId': game_id})

    # Pick side
    socketio_client.emit('pick_side', {'gameId': game_id, 'color': 'black', 'user': player.email})

    # Wait for computer move
    messages = socketio_client.get_received()

    # Check whether computer registers its own move
    last_update = list(filter(lambda message: message['name'] == 'update', messages))[-1]
    last_update_json_message = last_update['args'][0]
    assert len(last_update_json_message['board']['moves']) > 0
