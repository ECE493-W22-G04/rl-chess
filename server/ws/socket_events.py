from flask_socketio import SocketIO


def register_ws_events(socketio: SocketIO):

    @socketio.on("connect")
    def connect():
        # TODO: Remove this
        print("connected to client")

    @socketio.on("disconnect")
    def disconnect():
        # TODO: Remove this
        print("client disconnected")
