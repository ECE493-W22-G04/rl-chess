from flask import Blueprint, jsonify

index = Blueprint("index", __name__)


@index.route("/", methods=["POST", "GET"])
def handle_default():
    response_body = {
        "message": "Hello! I'm a message that came from the backend"}
    return jsonify(response_body), 200
