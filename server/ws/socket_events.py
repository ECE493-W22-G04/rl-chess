from flask_socketio import SocketIO


def register_ws_events(socketio: SocketIO):

    @socketio.on("connect")
    def connect():
        pass

    @socketio.on("disconnect")
    def disconnect():
        pass
