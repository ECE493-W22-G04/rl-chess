from flask import Blueprint, Flask, jsonify, request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from sqlalchemy import func

from ..models import Game, Player, SavedGame, db

leaderboard = Blueprint("leaderboard", __name__, url_prefix="/leaderboard")


@leaderboard.route("/", methods=["GET"])
@jwt_required()
def create_game():
    res = db.session.query(SavedGame.winner, func.count(SavedGame.winner)) \
        .group_by(SavedGame.winner) \
        .join(Player, SavedGame.winner == Player.id) \
        .add_columns(Player.email) \
        .group_by(Player.email) \
        .order_by(func.count(SavedGame.winner).desc()) \
        .all()
    payload = [{
        'email': email,
        'numWins': num_wins,
    } for [_id, num_wins, email] in res]
    return jsonify(payload), 200
