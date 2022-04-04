from flask_socketio import SocketIO

# local imports
from .api import create_app
from .ws.socket_events import register_ws_events

app = create_app()
# Set-up Socket.io
socketio = SocketIO(app, cors_allowed_origins="*")
register_ws_events(socketio)
