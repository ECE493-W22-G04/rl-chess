from pbu import Logger
from flask_socketio import SocketIO

from server.api import create_app
from server.ws.socket_events import register_ws_events
from server.api.config import get_log_folder

app = create_app()
# Set-up Socket.io
socketio = SocketIO(app, cors_allowed_origins="*")
register_ws_events(socketio)

if __name__ == "__main__":
    logger = Logger("MAIN", log_folder=get_log_folder())
    logger.info("==========================================")
    logger.info("           Starting application")
    logger.info("==========================================")

    # start flask app
    socketio.run(app, host="0.0.0.0", port="5555")
