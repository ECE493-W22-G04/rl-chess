import bcrypt
from sqlalchemy.exc import IntegrityError
from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token

from ..models import Player, db

auth = Blueprint("auth", __name__, url_prefix="/auth")

# This File is used to satisfy the following functional requirements:
# FR1 - User.Registration
# FR2 - Secure.Passwords
# FR4 - User.Login

# Create a route to authenticate users and return JWTs.
@auth.route("/signin", methods=["POST"])
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
            return jsonify({"access_token": access_token, "message": f"Welcome {email}"}), 200
        else:
            return jsonify({"message": "Incorrect password"}), 400
    except Exception as e:
        return jsonify({"message": f"Unsuccessful login attempt: {e}"}), 400


# Create a route to register a new user.
@auth.route("/signup", methods=["POST"])
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
        return jsonify({"message": f"Email already exists {email}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Unsuccessful registration attempt: {e}"}), 400


# Create a route to display a homepage message to an authenticated user
@auth.route("/user", methods=["GET"])
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
