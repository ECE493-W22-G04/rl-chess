import json
from flask_socketio import SocketIO
from flask import Flask
from flask.testing import FlaskClient
from flask_socketio.test_client import SocketIOTestClient
from pytest import fail

from server.api.models import Player
from server.game.move import Move, Square


def test_pvp_checkmate(socketio: SocketIO, socketio_client: SocketIOTestClient, client: FlaskClient, access_tokens: str, players: list[Player], app: Flask):
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

    # Pick side
    socketio_client2.emit('pick_side', {'gameId': game_id, 'color': 'white', 'user': players[0].email})

    # Fool's checkmate
    moves = [
        Move(Square(5, 6), Square(5, 4)),
        Move(Square(4, 1), Square(4, 3)),
        Move(Square(6, 6), Square(6, 4)),
        Move(Square(3, 0), Square(7, 4)),
    ]
    serialized_moves = list(map(lambda move : f'{move.from_square.x},{move.from_square.y}->{move.to_square.x},{move.to_square.y}', moves))
    for i, move in enumerate(serialized_moves):
        if i % 2 == 0:
            socketio_client.emit('make_move', {'gameId': game_id, 'moveStr': move, 'promotion': '0'})
        else:
            socketio_client2.emit('make_move', {'gameId': game_id, 'moveStr': move, 'promotion': '0'})

    messages1 = socketio_client.get_received()
    messages2 = socketio_client2.get_received()

    # Check the last message sent was a game over message
    for messages in [messages1, messages2]:
        last_message = messages[-1]
        if last_message['name'] != 'game_over':
            fail('Last message was not game over')
    
        json_message = json.loads(last_message['args'][0])
        winner = json_message['winner']
        assert winner == players[1].email

def test_draw(socketio: SocketIO, socketio_client: SocketIOTestClient, client: FlaskClient, access_tokens: str, players: list[Player], app: Flask):
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

    # Pick side
    socketio_client2.emit('pick_side', {'gameId': game_id, 'color': 'white', 'user': players[0].email})

    # Three fold repetition
    moves = [
        Move(Square(6, 7), Square(5, 5)),
        Move(Square(1, 0), Square(2, 2)),
        Move(Square(5, 5), Square(6, 7)),
        Move(Square(2, 2), Square(1, 0)),
    ] * 3
    serialized_moves = list(map(lambda move : f'{move.from_square.x},{move.from_square.y}->{move.to_square.x},{move.to_square.y}', moves))
    for i, move in enumerate(serialized_moves):
        if i % 2 == 0:
            socketio_client.emit('make_move', {'gameId': game_id, 'moveStr': move, 'promotion': '0'})
        else:
            socketio_client2.emit('make_move', {'gameId': game_id, 'moveStr': move, 'promotion': '0'})

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
