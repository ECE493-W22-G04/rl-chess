from pbu import Logger
from server.api.config import get_log_folder
from .__init__ import socketio, app

if __name__ == "__main__":
    logger = Logger("MAIN", log_folder=get_log_folder())
    logger.info("==========================================")
    logger.info("           Starting application")
    logger.info("==========================================")

    # start flask app
    socketio.run(app, host="0.0.0.0", port="5555")
