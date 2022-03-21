from flask import Blueprint, jsonify

game = Blueprint("games", __name__, url_prefix="/games")

GAME = {
    'id': 1,
    'blackPlayer': 'asfd@mail.com',
    'whitePlayer': 'asfd@mail.com',
    'game': None,
    'host': 'asfd@mail.com',
}


@game.route("/", methods=["POST"])
def create_game():
    # TODO: Generate game dynamically
    return jsonify(GAME), 201


@game.route("/<game_id>", methods=["GET"])
def get_game(game_id):
    # TODO: Get game dynamically
    return jsonify(GAME), 200
