from flask import Blueprint, jsonify, request

from .auth import auth
from .game import game

api = Blueprint("api", __name__, url_prefix="/api")
api.register_blueprint(auth)
api.register_blueprint(game)

# Create a route to display a homepage message to unauthenticated user
@api.route("/home", methods=["GET"])
def home():
    return jsonify({"message": "This is the generic homepage"}), 200


# Create a route to display a homepage message to an authenticated user
@api.route("/user", methods=["GET"])
def user():
    token = request.headers.get("authorization", None)
    # TODO: Check that token is valid
    if token:
        response_msg = 'This is the homepage of user with token: ' + token
        response_code = 200
    else:
        response_msg = 'token given in authorization header is invalid'
        response_code = 401
    return jsonify({"message": response_msg}), response_code
