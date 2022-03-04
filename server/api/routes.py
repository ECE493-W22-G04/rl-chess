from flask import Flask, request, jsonify, url_for, Blueprint

routes = Blueprint("routes", __name__)


@routes.route("/", methods=["POST", "GET"])
def handle_default():
    response_body = {"message": "This is the default route for this app, you can write more routes here"}
    return jsonify(response_body), 200


@routes.route("/hello", methods=["POST", "GET"])
def handle_hello():

    response_body = {"message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"}

    return jsonify(response_body), 200
