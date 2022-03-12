import os

from sqlalchemy.exc import IntegrityError
import bcrypt

from flask import Flask, request, jsonify, url_for, Blueprint
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from api.models import Player, db

api = Blueprint("api", __name__)


@api.route("/", methods=["POST", "GET"])
def handle_default():
    response_body = {"message": "Hello! I'm a message that came from the backend"}
    return jsonify(response_body), 200


# Create a route to authenticate users and return JWTs.
@api.route("/api/auth/signin", methods=["POST"])
def signin():
    try:
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        if not email:
            return jsonify({"message": "No email provided!"}), 400
        if not password:
            return jsonify({"message": "No password provided"}), 400

        player = Player.query.filter_by(email=email).first()

        if not player:
            return jsonify({"message": "Email not found"}), 400
        
        if bcrypt.checkpw(password.encode('utf-8'), player.password.encode('utf-8')):
            access_token = create_access_token(identity=email)
            return jsonify({access_token: access_token, "message": f"Welcome {email}"}), 200
        else:
            return jsonify({"message": "Incorrect password"}), 400
    except:
        db.session.rollback()
        return jsonify({"message": "Unsuccessful login attempt"}), 400
    

# Create a route to register a new user.
@api.route("/api/auth/signup", methods=["POST"])
def signup():
    try:
        if request.is_json:
            email = request.json.get("email", None)
            password = request.json.get("password", None)

            if not email:
                return jsonify({"message": "No email provided!"}), 400
            if not password:
                return jsonify({"message": "No password provided"}), 400

            # Hash password and store hashed value in db
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            new_player = Player(email=email, password=hashed.decode('utf-8'))

            # Put new player in database
            db.session.add(new_player)
            db.session.commit()
            return jsonify({"message": f"Registration Successful {email}!"}), 200
        else:
            return jsonify({"message": "The payload is not in JSON format"}), 400
    except IntegrityError:
        # Catch error where email already exists
        # rollback reverts the changes made to the db
        db.session.rollback()
        return jsonify({"message": "Email already exists"}), 400
    except:
        db.session.rollback()
        return jsonify({"message": "Unsuccessful login attempt"}), 400


# Create a route to display a homepage message to unauthenticated user
@api.route("/api/home", methods=["GET"])
def home():
    return jsonify({"message": "This is the generic homepage"}), 200


# Create a route to display a homepage message to an authenticated user
@api.route("/api/user", methods=["GET"])
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
