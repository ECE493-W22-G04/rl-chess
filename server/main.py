from flask import Flask
from flask_cors import CORS
from flask import jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from config import load_config, get_log_folder
from pbu import Logger
from api.routes import api


def create_app():
    # load config from .env file
    config = load_config()
    app = Flask(__name__)
    CORS(app)

    # Setup the Flask-JWT-Extended extension
    app.config["JWT_SECRET_KEY"] = config["JWT_SECRET_KEY"]
    jwt = JWTManager(app)

    app.register_blueprint(api)

    return app


def main():
    logger = Logger("MAIN", log_folder=get_log_folder())
    logger.info("==========================================")
    logger.info("           Starting application")
    logger.info("==========================================")

    app = create_app()

    # start flask app
    app.run(host="0.0.0.0", port=5555)


if __name__ == "__main__":
    main()
