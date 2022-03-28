from uuid import UUID
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from api.models import Game
from api.exceptions import PlayerDoesNotExist

game = Blueprint("games", __name__, url_prefix="/games")

current_games: dict[str, Game] = {}


@game.route("/", methods=["POST"])
@jwt_required()
def create_game():
    current_user = get_jwt_identity()
    try:
        game = Game(host_email=current_user)
    except PlayerDoesNotExist:
        return jsonify(game.toJSON()), 400
    current_games[game.id] = game
    return jsonify(game.toJSON()), 201


@game.route("/<game_id>", methods=["GET"])
@jwt_required()
def get_game(game_id):
    if not game_id in current_games:
        return jsonify({}), 404
    return jsonify(current_games[game_id].toJSON()), 200
