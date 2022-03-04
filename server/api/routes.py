import os

from flask import Flask, request, jsonify, url_for, Blueprint
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

api = Blueprint("api", __name__)

@api.route("/", methods=["POST", "GET"])
def handle_default():
    response_body = {"message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"}
    return jsonify(response_body), 200


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@api.route("/api/auth/signin", methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    # TODO: Check database for email and password
    if email != "test@test.test" or password != "test123test":
        return jsonify({"message": "Bad username or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)

# Create a route to register a new user.
@api.route("/api/auth/signup", methods=["POST"])
def signup():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    # TODO: Put email and password in database
    # TODO: Return error if email already exists
    if email != "test@test.test" or password != "test123test":
        return jsonify({"message": "Bad username or password"}), 401

    return jsonify({"message": "Registration Successful!"}), 200

# Create a route to display a homepage message to unauthenticated user
@api.route("/api/home", methods=["GET"])
def home():
    return jsonify({"message": "This is the generic homepage"}), 200

# Create a route to display a homepage message to an authenticated user
@api.route("/api/user", methods=["GET"])
def user():
    token = request.headers.get("authorization", None)
    # TODO: Check that token is valid
    response_msg = 'This is the homepage of user with token: ' + token
    return jsonify({"message": response_msg}), 200