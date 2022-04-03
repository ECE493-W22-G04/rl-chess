from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from sqlalchemy.sql import func

from ..models import SavedGame, db

leaderboard = Blueprint("leaderboard", __name__, url_prefix="/leaderboard")


@leaderboard.route("/", methods=["GET"])
def get_leaderboard():
    data = db.session.query(SavedGame.winner, func.count(SavedGame.winner)).group_by(SavedGame.winner).all()
    print(data)
    return jsonify({}), 201
