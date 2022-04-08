from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
import json

from ..models import Game
from ..exceptions import PlayerDoesNotExist

game = Blueprint("games", __name__, url_prefix="/games")

current_games: dict[str, Game] = {}

# This File is used to satisfy the following functional requirements:
# FR10 - Initialize.Lobby
# FR11 - Generate.Link
# FR13 - Allow.Authentic.Users


@game.route("/", methods=["POST"])
@jwt_required()
def create_game():
    current_user = get_jwt_identity()
    is_pvp = request.json['isPvP']
    try:
        game = Game(host_email=current_user, is_pvp=is_pvp)
    except PlayerDoesNotExist:
        err_msg = '{"err": "Player does not exist"}'
        return jsonify(err_msg), 400
    current_games[game.id] = game
    return jsonify(game.toJSON()), 201


@game.route("/<game_id>", methods=["GET"])
@jwt_required()
def get_game(game_id):
    if not game_id in current_games:
        return jsonify({}), 404
    return jsonify(current_games[game_id].toJSON()), 200
