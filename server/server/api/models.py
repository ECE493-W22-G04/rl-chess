import json
from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .exceptions import PlayerDoesNotExist
from ..game.board import Board

db = SQLAlchemy()
migrate = Migrate()


class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Player {self.email}>"


# Not sure if this can work with the Game model defined, we store slightly different information, cleaner separate?
class SavedGame(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    # null player means RL
    black_player = db.Column(db.Integer, db.ForeignKey("players.id"), nullable=True)
    white_player = db.Column(db.Integer, db.ForeignKey("players.id"), nullable=True)
    winner = db.Column(db.Integer, db.ForeignKey("players.id"), nullable=True)  # null winner means draw
    game_history = db.Column(db.Text)
    is_pvp = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"<Game {self.id}>"


class Game():

    def __init__(self, host_email: int, is_pvp: bool = False) -> None:
        self.id = str(uuid4())
        if Player.query.filter_by(email=host_email).first() == None:
            raise PlayerDoesNotExist()
        self.host = host_email
        self.black_player = None
        self.white_player = None
        self.board = Board()
        self.is_pvp = is_pvp
        self.has_started = False

    def start_game(self) -> None:
        self.has_started = True

    def toJSON(self) -> dict:
        return {
            'id': self.id,
            'host': self.host,
            'black_player': self.black_player,
            'white_player': self.white_player,
            'board': self.board.toJSON(),
            'is_pvp': self.is_pvp,
            'has_started': self.has_started,
        }

    def set_white_player(self, player_email: str):
        if Player.query.filter_by(email=player_email).first() == None:
            raise PlayerDoesNotExist()
        self.white_player = player_email

    def set_black_player(self, player_email: str):
        if Player.query.filter_by(email=player_email).first() == None:
            raise PlayerDoesNotExist()
        self.black_player = player_email
