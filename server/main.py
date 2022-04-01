from pbu import Logger
from flask_socketio import SocketIO

# local imports
from api import create_app
from ws.socket_events import register_ws_events
from api.config import get_log_folder
from .rl_agent.agent import RlAgent

app = create_app()
# Set-up Socket.io
socketio = SocketIO(app, cors_allowed_origins="*")
register_ws_events(socketio)

rl_agent = RlAgent()

if __name__ == "__main__":
    logger = Logger("MAIN", log_folder=get_log_folder())
    logger.info("==========================================")
    logger.info("           Starting application")
    logger.info("==========================================")

    # start flask app
    socketio.run(app, host="0.0.0.0", port="5555")
