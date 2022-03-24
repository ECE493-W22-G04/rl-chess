from flask_socketio import SocketIO, join_room, leave_room, send

user_rooms = {}


def register_ws_events(socketio: SocketIO):

    @socketio.on("connect")
    def connect():
        pass

    @socketio.on("disconnect")
    def disconnect():
        pass

    @socketio.on("join")
    def on_join(data):
        user = data["user"]
        game_id = data["gameId"]

        # only let a player join a room a single time (fixes bug of 2 join calls for each connect)
        if (game_id in user_rooms.keys()) and (user in user_rooms[game_id]):
            return
        if game_id in user_rooms.keys():
            user_rooms[game_id].append(user)
        else:
            user_rooms[game_id] = [user]

        print(user_rooms)
        join_room(game_id)
        send(user + " has joined the room", to=game_id)
