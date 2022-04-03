import os
from dotenv import load_dotenv

DEFAULTS = {"JWT_SECRET_KEY": "", "LOG_FOLDER": "_logs", "IS_DEBUG": False,
            "DATABASE_URL": "postgresql://postgres:postgres@localhost:5432/postgres"}


def load_config():
    load_dotenv()
    config = {
        "JWT_SECRET_KEY": os.getenv("JWT_SECRET_KEY"),
        "LOG_FOLDER": os.getenv("LOG_FOLDER"),
        "IS_DEBUG": os.getenv("IS_DEBUG") == "1",
        # Heroku defaults to using postgres:// but that is no longer supported
        # Only postgresql:// is supported in latest SQLAlchemy version
        "DATABASE_URL": os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1),
    }

    # apply defaults for missing config params
    for key in DEFAULTS:
        if key not in config or config[key] is None:
            config[key] = DEFAULTS[key]

    # check if log folder exists
    if not os.path.isdir(config["LOG_FOLDER"]):
        os.mkdir(config["LOG_FOLDER"])

    return config


def get_log_folder():
    config = load_config()
    return config["LOG_FOLDER"]


def is_debug():
    config = load_config()
    return config["IS_DEBUG"]
