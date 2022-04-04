import json
from flask import Flask
import pytest
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token

from server.api.models import Game, SavedGame, Player, db
from ..constants import TEST_EMAIL, TEST_PASSWORD


def test_leaderboard(client: FlaskClient, app: Flask):
    with app.app_context():
        player1 = Player(email=TEST_EMAIL, password=TEST_PASSWORD)
        player2 = Player(email='asdf@mail.com', password=TEST_PASSWORD)
        for player in [player1, player2]:
            db.session.add(player)
            db.session.commit()

        pvc_game = Game(host_email=player.email, is_pvp=False)
        saved_game1 = SavedGame(black_player=player1.id, white_player=None, winner=player1.id, game_history=json.dumps(pvc_game.board.moves), is_pvp=pvc_game.is_pvp)
        saved_game2 = SavedGame(black_player=player1.id, white_player=None, winner=player1.id, game_history=json.dumps(pvc_game.board.moves), is_pvp=pvc_game.is_pvp)
        saved_game3 = SavedGame(black_player=player2.id, white_player=None, winner=None, game_history=json.dumps(pvc_game.board.moves), is_pvp=pvc_game.is_pvp)
        for saved_game in [saved_game1, saved_game2, saved_game3]:
            db.session.add(saved_game)
            db.session.commit()

        resp = client.get('/api/leaderboard/')
        json_response = resp.json

        expected_payloads = [{
            'email': player1.email,
            'numWins': 2,
        }]
        assert resp.status_code == 200
        for expected_payload in expected_payloads:
            assert expected_payload in json_response


def test_empty_leaderboard(client: FlaskClient, app: Flask):
    with app.app_context():
        resp = client.get('/api/leaderboard/')
        json_response = resp.json

        expected_payloads = []
        assert resp.status_code == 200
        for expected_payload in expected_payloads:
            assert expected_payload in json_response
