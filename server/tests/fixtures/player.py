from flask import Flask
from flask_jwt_extended import create_access_token
import pytest

from server.api.models import Player, db
from ..constants import TEST_EMAIL, TEST_EMAIL2, TEST_EMAIL3, TEST_EMAIL4, TEST_PASSWORD


@pytest.fixture
def player(app: Flask) -> Player:
    with app.app_context():
        player = Player(email=TEST_EMAIL, password=TEST_PASSWORD)
        db.session.add(player)
        db.session.commit()

        yield player


@pytest.fixture
def missing_player(app: Flask) -> Player:
    with app.app_context():
        player = Player(email=TEST_EMAIL4, password=TEST_PASSWORD)

        yield player


@pytest.fixture
def players(app: Flask) -> Player:
    with app.app_context():
        player1 = Player(email=TEST_EMAIL2, password=TEST_PASSWORD)
        player2 = Player(email=TEST_EMAIL3, password=TEST_PASSWORD)
        db.session.add(player1)
        db.session.add(player2)
        db.session.commit()
        yield [player1, player2]


@pytest.fixture
def access_token(player: Player) -> str:
    yield create_access_token(identity=player.email)


@pytest.fixture
def missing_player_access_token(missing_player: Player) -> str:
    yield create_access_token(identity=missing_player.email)


@pytest.fixture
def access_tokens(players: list[Player]) -> Player:
    yield [create_access_token(identity=player.email) for player in players]
