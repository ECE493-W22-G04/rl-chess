from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from server.api.config import load_config, get_log_folder
from server.api.routes.api import api
from server.api.routes.index import index
from server.api.models import db


def create_app():
    # load config from .env file
    config = load_config()

    # create app
    app = Flask(__name__)
    CORS(app)

    # Setup the Flask-JWT-Extended extension
    app.config["JWT_SECRET_KEY"] = config["JWT_SECRET_KEY"]

    # Setup the SQLALCHEMY configuration
    app.config["SECRET_KEY"] = config["JWT_SECRET_KEY"]
    app.config["SQLALCHEMY_DATABASE_URI"] = config["DATABASE_URL"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.register_blueprint(index)
    app.register_blueprint(api)

    # Set-up SQLAlchemy
    db.init_app(app)
    migrate = Migrate(app, db)
    with app.app_context():
        db.drop_all()  # Clears all tables and resets them, possibly later we will want to migrate
        db.create_all()

    # Set-up JWT manager
    jwt = JWTManager(app)
    return app
