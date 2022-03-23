from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy

from .exceptions import PlayerDoesNotExist

db = SQLAlchemy()


class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Player {self.email}>"


class Game:

    def __init__(self, host_email: int) -> None:
        self.id = uuid4()
        if Player.query.filter_by(email=host_email).first() == None:
            raise PlayerDoesNotExist()
        self.host = host_email
        self.black_player = None
        self.white_player = None

    def set_white_player(self, player_email: int):
        if Player.query.filter_by(email=player_email).first() == None:
            raise PlayerDoesNotExist()
        self.white_player = player_email

    def set_black_player(self, player_email: int):
        if Player.query.filter_by(email=player_email).first() == None:
            raise PlayerDoesNotExist()
        self.black_player = player_email
