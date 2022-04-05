import json
from flask import Flask
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token

from server.api.models import Game, SavedGame, Player, db
from ..constants import TEST_EMAIL, TEST_PASSWORD


def test_leaderboard_unauthed(client: FlaskClient):
    resp = client.get('/api/leaderboard/')
    assert resp.status_code == 401


def test_leaderboard_excludes_players_with_less_than_4_wins(client: FlaskClient, app: Flask):
    with app.app_context():
        player1 = Player(email=TEST_EMAIL, password=TEST_PASSWORD)
        player2 = Player(email='asdf@mail.com', password=TEST_PASSWORD)
        for player in [player1, player2]:
            db.session.add(player)
            db.session.commit()

        player1_access_token = create_access_token(identity=player.email)

        pvc_game = Game(host_email=player.email, is_pvp=False)
        num_player_1_wins = 12
        num_player_1_losses = 2
        for i in range(num_player_1_wins):
            saved_game = SavedGame(black_player=player1.id, white_player=None, winner=player1.id, game_history=json.dumps(pvc_game.board.moves), is_pvp=pvc_game.is_pvp)
            db.session.add(saved_game)
            db.session.commit()
        for i in range(num_player_1_losses):
            saved_game = SavedGame(black_player=player1.id, white_player=None, winner=None, game_history=json.dumps(pvc_game.board.moves), is_pvp=pvc_game.is_pvp)
            db.session.add(saved_game)
            db.session.commit()
        num_player_2_wins = 4
        for i in range(num_player_2_wins):
            saved_game = SavedGame(black_player=player2.id, white_player=None, winner=player2.id, game_history=json.dumps(pvc_game.board.moves), is_pvp=pvc_game.is_pvp)
            db.session.add(saved_game)
            db.session.commit()

        resp = client.get('/api/leaderboard/', headers={'Authorization': f'Bearer {player1_access_token}'})
        json_response = resp.json

        expected_payload = [{
            'email': player1.email,
            'numGamesWon': num_player_1_wins,
            'numGamesPlayed': num_player_1_wins + num_player_1_losses,
            'winRate': num_player_1_wins / (num_player_1_wins + num_player_1_losses),
        }]

        resp = client.get('/api/leaderboard/', headers={'Authorization': f'Bearer {player1_access_token}'})
        json_response = resp.json

        assert resp.status_code == 200
        assert expected_payload == json_response


def test_empty_leaderboard(client: FlaskClient, app: Flask, access_token: str):
    resp = client.get('/api/leaderboard/', headers={'Authorization': f'Bearer {access_token}'})
    json_response = resp.json

    expected_payload = []
    assert resp.status_code == 200
    assert expected_payload == json_response


def test_leaderboard_ordering(client: FlaskClient, app: Flask):
    with app.app_context():
        player1 = Player(email=TEST_EMAIL, password=TEST_PASSWORD)
        player2 = Player(email='asdf@mail.com', password=TEST_PASSWORD)
        for player in [player1, player2]:
            db.session.add(player)
            db.session.commit()

        player1_access_token = create_access_token(identity=player.email)

        pvc_game = Game(host_email=player.email, is_pvp=False)
        num_player_1_wins = 12
        num_player_1_losses = 2
        for i in range(num_player_1_wins):
            saved_game = SavedGame(black_player=player1.id, white_player=None, winner=player1.id, game_history=json.dumps(pvc_game.board.moves), is_pvp=pvc_game.is_pvp)
            db.session.add(saved_game)
            db.session.commit()
        for i in range(num_player_1_losses):
            saved_game = SavedGame(black_player=player1.id, white_player=None, winner=None, game_history=json.dumps(pvc_game.board.moves), is_pvp=pvc_game.is_pvp)
            db.session.add(saved_game)
            db.session.commit()
        num_player_2_wins = 10
        for i in range(num_player_2_wins):
            saved_game = SavedGame(black_player=player2.id, white_player=None, winner=player2.id, game_history=json.dumps(pvc_game.board.moves), is_pvp=pvc_game.is_pvp)
            db.session.add(saved_game)
            db.session.commit()

        resp = client.get('/api/leaderboard/', headers={'Authorization': f'Bearer {player1_access_token}'})
        json_response = resp.json

        assert resp.status_code == 200
        assert sorted(json_response, key=lambda x: x['winRate'], reverse=True) == json_response


def test_leaderboard_excludes_pvp_games(client: FlaskClient, app: Flask):
    with app.app_context():
        player1 = Player(email=TEST_EMAIL, password=TEST_PASSWORD)
        player2 = Player(email='asdf@mail.com', password=TEST_PASSWORD)
        for player in [player1, player2]:
            db.session.add(player)
            db.session.commit()

        player1_access_token = create_access_token(identity=player.email)

        pvp_game = Game(host_email=player.email, is_pvp=True)
        saved_game = SavedGame(black_player=player1.id, white_player=player2.id, winner=player1.id, game_history=json.dumps(pvp_game.board.moves), is_pvp=pvp_game.is_pvp)
        db.session.add(saved_game)
        db.session.commit()

        resp = client.get('/api/leaderboard/', headers={'Authorization': f'Bearer {player1_access_token}'})
        json_response = resp.json

        expected_payload = []
        assert resp.status_code == 200
        assert json_response == expected_payload
