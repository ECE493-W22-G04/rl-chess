from flask import Flask
from flask_jwt_extended import create_access_token
import pytest

from server.api.models import Player, db
from ..constants import TEST_EMAIL, TEST_PASSWORD


@pytest.fixture
def player(app: Flask) -> Player:
    with app.app_context():
        player = Player(email=TEST_EMAIL, password=TEST_PASSWORD)
        db.session.add(player)
        db.session.commit()

        yield player


@pytest.fixture
def access_token(player: Player) -> str:
    yield create_access_token(identity=player.email)
