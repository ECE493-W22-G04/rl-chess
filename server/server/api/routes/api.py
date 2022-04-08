from flask import Blueprint

from .auth import auth
from .games import game
from .leaderboard import leaderboard

api = Blueprint("api", __name__, url_prefix="/api")
api.register_blueprint(auth)
api.register_blueprint(game)
api.register_blueprint(leaderboard)
