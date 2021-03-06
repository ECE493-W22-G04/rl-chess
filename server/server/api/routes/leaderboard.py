from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import func, cast, Float

from ..models import Game, Player, SavedGame, db

leaderboard = Blueprint("leaderboard", __name__, url_prefix="/leaderboard")

MIN_GAMES_UNTIL_LEADERBOARD = 10


@leaderboard.route("/", methods=["GET"])
@jwt_required()
def create_game():
    res = db.session.query(Player.id,
            func.count(SavedGame.winner == Player.id),
            func.count(SavedGame.id),
            cast(func.count(SavedGame.winner == Player.id), Float) / cast(func.count(SavedGame.id), Float),
        ) \
        .filter(SavedGame.is_pvp==False) \
        .group_by(Player.id) \
        .join(Player, (SavedGame.black_player == Player.id) | (SavedGame.white_player == Player.id)) \
        .add_columns(Player.email) \
        .group_by(Player.email) \
        .having(func.count(SavedGame.id) >= MIN_GAMES_UNTIL_LEADERBOARD) \
        .order_by((cast(func.count(SavedGame.winner == Player.id), Float) / cast(func.count(SavedGame.id), Float)).desc())
    payload = [{
        'email': email,
        'numGamesWon': num_games_won,
        'numGamesPlayed': num_games_played,
        'email': email,
        'winRate': win_rate,
    } for [_id, num_games_won, num_games_played, win_rate, email] in res.all()]
    return jsonify(payload), 200
