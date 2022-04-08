import json
from flask_socketio import SocketIO
from flask import Flask
from flask.testing import FlaskClient
from flask_socketio.test_client import SocketIOTestClient
from pytest import fail

from server.api.models import Player, SavedGame


def test_updates_players_in_room(socketio: SocketIO, socketio_client: SocketIOTestClient, client: FlaskClient, access_tokens: str, players: list[Player], app: Flask):
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

    # Disconnect from game
    socketio_client2.disconnect()

    messages = socketio_client.get_received()

    players_in_room_message_count = 0
    room_not_full_message_count = 0
    for message in messages:
        if message['name'] == 'players_in_room':
            players_in_room_message_count += 1
        if message['name'] == 'room_not_full':
            room_not_full_message_count += 1
    assert players_in_room_message_count == 3  # First message when player[0] joins, second when player[1] joins, finally when player[1] disconnects
    assert room_not_full_message_count == 1


def test_ends_ongoing_game(socketio: SocketIO, socketio_client: SocketIOTestClient, client: FlaskClient, access_tokens: str, players: list[Player], app: Flask):
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

    # Disconnect from game
    socketio_client2.disconnect()

    messages = socketio_client.get_received()

    for message in messages:
        if message['name'] == 'game_over':
            message_body = json.loads(message['args'][0])
            winner = message_body['winner']
            assert winner == players[0].email
            return
    fail('Game over was not issued for the remaining player')


def test_computer_wins(app: Flask, socketio_client: SocketIOTestClient, client: FlaskClient, access_token: str, player: list[Player]):
    # Create computer game
    resp = client.post('/api/games/', data=json.dumps({'isPvP': False}), headers={'Authorization': f'Bearer {access_token}'}, content_type='application/json')
    assert resp.status_code == 201
    game = resp.json
    game_id = game['id']

    # Join game
    socketio_client.emit('join', {'user': player.email, 'gameId': game_id})

    # Start game
    socketio_client.emit('pick_side', {'gameId': game_id, 'color': 'white', 'user': player.email})

    # Disconnect from game
    socketio_client.disconnect()

    with app.app_context():
        assert len(SavedGame.query.all()) == 1
        saved_game = SavedGame.query.first()
        assert saved_game.white_player == player.id
        assert saved_game.black_player == None
        assert saved_game.winner == None  # Equivalent to computer winning


def test_deletes_game_after_game_has_started(app: Flask, socketio_client: SocketIOTestClient, client: FlaskClient, access_token: str, player: list[Player]):
    # Create computer game
    resp = client.post('/api/games/', data=json.dumps({'isPvP': False}), headers={'Authorization': f'Bearer {access_token}'}, content_type='application/json')
    assert resp.status_code == 201
    game = resp.json
    game_id = game['id']

    # Join game
    socketio_client.emit('join', {'user': player.email, 'gameId': game_id})

    # Start game
    socketio_client.emit('pick_side', {'gameId': game_id, 'color': 'white', 'user': player.email})

    # Disconnect from game
    socketio_client.disconnect()

    resp = client.get(f'/api/games/{game_id}', headers={'Authorization': f'Bearer {access_token}'})
    assert resp.status_code == 404


def test_deletes_game_before_game_has_started(app: Flask, socketio_client: SocketIOTestClient, client: FlaskClient, access_token: str, player: list[Player]):
    # Create computer game
    resp = client.post('/api/games/', data=json.dumps({'isPvP': False}), headers={'Authorization': f'Bearer {access_token}'}, content_type='application/json')
    assert resp.status_code == 201
    game = resp.json
    game_id = game['id']

    # Join game
    socketio_client.emit('join', {'user': player.email, 'gameId': game_id})

    # Disconnect from game
    socketio_client.disconnect()

    resp = client.get(f'/api/games/{game_id}', headers={'Authorization': f'Bearer {access_token}'})
    assert resp.status_code == 404


def test_keeps_game_when_one_player_remains(socketio: SocketIO, socketio_client: SocketIOTestClient, client: FlaskClient, access_tokens: str, players: list[Player], app: Flask):
    resp = client.post('/api/games/', data=json.dumps({'isPvP': True}), headers={'Authorization': f'Bearer {access_tokens[0]}'}, content_type='application/json')
    assert resp.status_code == 201
    game = resp.json
    game_id = game['id']

    # Create second client
    socketio_client2 = socketio.test_client(app, flask_test_client=client)

    # Join game
    socketio_client.emit('join', {'user': players[0].email, 'gameId': game_id})
    socketio_client2.emit('join', {'user': players[1].email, 'gameId': game_id})

    # Disconnect from game
    socketio_client2.disconnect()

    resp = client.get(f'/api/games/{game_id}', headers={'Authorization': f'Bearer {access_tokens[0]}'})
    assert resp.status_code == 200
