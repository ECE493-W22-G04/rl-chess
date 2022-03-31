from flask_socketio import SocketIO, join_room, leave_room, emit
from api.routes.games import current_games
from game.move import Move, Square
from flask import current_app, request

# TODO: set PLAYERS_PER_ROOM based on game type
PLAYERS_PER_ROOM = 2

user_rooms: dict[str, list[str]] = {}
socket_id_to_user_map: dict[str, str] = {}
user_to_room_map: dict[str, str] = {}


def register_ws_events(socketio: SocketIO):

    @socketio.on("connect")
    def connect():
        pass

    @socketio.on("disconnect")
    def disconnect():
        user = socket_id_to_user_map.get(request.sid)
        if user == None:
            return

        socket_id_to_user_map.pop(request.sid)
        game_id = user_to_room_map.get(user)
        users_in_room = user_rooms.get(game_id)
        if users_in_room == None:
            return

        if len(users_in_room) == 0:
            user_rooms.pop(game_id)
            current_games.pop(game_id)
            return

    @socketio.on("join")
    def on_join(data):
        user = data["user"]
        game_id = data["gameId"]

        socket_id_to_user_map[request.sid] = user

        # only let a player join a room a single time (fixes bug of 2 join calls for each connect)
        if (game_id in user_rooms.keys()) and (user in user_rooms[game_id]):
            return
        if game_id in user_rooms.keys():
            # Don't allow others to join full room
            if len(user_rooms[game_id]) == PLAYERS_PER_ROOM:
                return
            user_rooms[game_id].append(user)
        else:
            user_rooms[game_id] = [user]

        join_room(game_id)
        emit("message", user + " has joined the room", broadcast=True, to=game_id)

        if (len(user_rooms[game_id]) == PLAYERS_PER_ROOM):
            emit("room_full", broadcast=True, to=game_id)

    @socketio.on("pick_side")
    def pick_side(data):
        game_id = data["gameId"]
        color = data["color"]
        user = data["user"]
        other_user = ""

        # check game exists
        if game_id not in current_games or game_id not in user_rooms:
            emit("message", "Attempted to pick color with invalid game id " + game_id, broadcast=True, to=game_id)
            return

        for user_in_room in user_rooms[game_id]:
            if user_in_room != user:
                other_user = user_in_room
                break

        # check if player in room and is host of current game
        if user in user_rooms[game_id] and user == current_games[game_id].host:
            if color == "white":
                current_games[game_id].set_white_player(user)
                current_games[game_id].set_black_player(other_user)
            elif color == "black":
                current_games[game_id].set_black_player(user)
                current_games[game_id].set_white_player(other_user)
        emit('start_game', current_games[game_id].toJSON(), broadcast=True, to=game_id)

    @socketio.on("make_move")
    def make_move(data):
        game_id = data["gameId"]
        # move_str looks like 'x,y->x,y'
        move_str = data["moveStr"]

        # check game exists
        if game_id not in current_games:
            emit("message", "Attempted to make move with invalid game id " + game_id, broadcast=True, to=game_id)
            return

        # check if move is valid
        (move_from, move_to) = move_str.split("->")
        (from_x, from_y) = move_from.split(",")
        (to_x, to_y) = move_to.split(",")
        move = Move(Square(int(from_x), int(from_y)), Square(int(to_x), int(to_y)))
        if current_games[game_id].board.register_move(move):
            emit('update', current_games[game_id].toJSON(), broadcast=True, to=game_id)
        else:
            emit("message", "Invalid move " + move_str, to=game_id)
