from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

from server.api.exceptions import PlayerDoesNotExist

db = SQLAlchemy()


class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Player {self.email}>"


class Game:

    def __init__(self, host_player_id: int) -> None:
        self.id = uuid4()
        if Player.query.get(host_player_id) == None:
            raise PlayerDoesNotExist()
        self.host = host_player_id
        self.black_player = None
        self.white_player = None

    def set_white_player(self, player_id: int):
        if Player.query.get(player_id) == None:
            raise PlayerDoesNotExist()
        self.white_player = player_id

    def set_black_player(self, player_id: int):
        if Player.query.get(player_id) == None:
            raise PlayerDoesNotExist()
        self.black_player = player_id
