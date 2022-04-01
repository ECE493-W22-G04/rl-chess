from flask_socketio import SocketIO, join_room, leave_room, emit
from numpy import broadcast

from ..game.move import Move, Square
from ..api.routes.games import current_games
from ..main import rl_agent

PLAYERS_PER_PVP_ROOM = 2
PLAYERS_PER_PVC_ROOM = 1

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

        if game_id not in current_games:
            emit('error', 'Game no longer exists', broadcast=True, to=game_id)
            return

        game = current_games[game_id]

        # only let a player join a room a single time (fixes bug of 2 join calls for each connect)
        if (game_id in user_rooms.keys()) and (user in user_rooms[game_id]):
            return

        def is_room_full(is_pvp: bool, num_players_in_room: int):
            if game.is_pvp:
                return num_players_in_room == PLAYERS_PER_PVP_ROOM
            return num_players_in_room == PLAYERS_PER_PVC_ROOM

        if game_id in user_rooms:
            if is_room_full(game.is_pvp, len(user_rooms[game_id])):
                # Prevent users from joining full room
                return

            user_rooms[game_id].append(user)
        else:
            user_rooms[game_id] = [user]

        join_room(game_id)
        emit("message", user + " has joined the room", broadcast=True, to=game_id)

        if is_room_full(game.is_pvp, len(user_rooms[game_id])):
            emit("room_full", broadcast=True, to=game_id)

    @socketio.on("pick_side")
    def pick_side(data):
        game_id = data["gameId"]
        color = data["color"]
        user = data["user"]
        other_user = None

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

        # Make first move as computer
        game = current_games[game_id]
        if game.is_pvp:
            return    
        if game.white_player == user:
            return
        rl_move = rl_agent.predict(game.board)
        game.board.register_move(rl_move)

        emit('update', game.toJSON(), broadcast=True, to=game_id)
        

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
        game = current_games[game_id]
        if game.board.register_move(move):
            emit('update', current_games[game_id].toJSON(), broadcast=True, to=game_id)
        else:
            emit("message", "Invalid move " + move_str, to=game_id)

        # Make computer move
        if game.is_pvp:
            return
        rl_move = rl_agent.predict(game.board)
        game.board.register_move(rl_move)
        emit('update', game.toJSON(), broadcast=True, to=game_id)
