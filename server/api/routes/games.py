from uuid import UUID
from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from api.models import Game

game = Blueprint("games", __name__, url_prefix="/games")

GAME = {
    "id": 1,
    "blackPlayer": "asfd@mail.com",
    "whitePlayer": "asfd@mail.com",
    "game": None,
    "host": "asfd@mail.com",
}

current_games: dict[UUID, Game] = {}


@game.route("/", methods=["POST"])
@jwt_required()
def create_game():
    current_user = get_jwt_identity()
    game = Game(host_email=current_user)
    current_games[game.id] = game
    return jsonify(game.__dict__), 201


@game.route("/<game_id>", methods=["GET"])
@jwt_required()
def get_game(game_id):
    game_uuid = UUID(game_id)
    if not game_uuid in current_games:
        return jsonify({}), 404
    return jsonify(current_games[game_uuid].__dict__), 200
