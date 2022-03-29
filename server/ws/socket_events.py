from flask_socketio import SocketIO, join_room, leave_room, emit
from api.routes.games import current_games
from game.move import Move, Square

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
        # TODO: set expected players based on game type 
        expected_players = 2
        user = data["user"]
        game_id = data["gameId"]

        # only let a player join a room a single time (fixes bug of 2 join calls for each connect)
        if (game_id in user_rooms.keys()) and (user in user_rooms[game_id]):
            return
        if game_id in user_rooms.keys():
            if len(user_rooms[game_id]) < expected_players:
                user_rooms[game_id].append(user)
            else:
                join_room(game_id)
                emit("message", user + " attempted to join this full room", broadcast=True, to=game_id)
                leave_room(game_id)
                return
        else:
            user_rooms[game_id] = [user]

        print(user_rooms)
        join_room(game_id)
        emit("message", user + " has joined the room", broadcast=True, to=game_id)
        
        if (len(user_rooms[game_id]) == expected_players):
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
        emit("message", "White player: " + current_games[game_id].white_player, broadcast=True, to=game_id)
        emit("message", "Black player: " + current_games[game_id].black_player, broadcast=True, to=game_id)
        emit('start_game', None, broadcast=True, to=game_id)

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
            emit("message", "Invalid move " + move_str, broadcast=True, to=game_id)

        
