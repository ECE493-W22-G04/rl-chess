from flask_socketio import SocketIO, join_room, leave_room, emit
from api.routes.games import current_games
from game.move import Move, Square

from api.models import SavedGame, Player, db

# TODO: set PLAYERS_PER_ROOM based on game type
PLAYERS_PER_ROOM = 2

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
        current_game = current_games[game_id]
        if current_game.board.register_move(move):
            emit('update', current_game.toJSON(), broadcast=True, to=game_id)
            if current_game.board.is_checkmate():
                is_white_turn = not current_game.board.is_white_turn  # opposite because it registered move
                winner = "White" if is_white_turn else "Black"
                # TODO: handle this emit client side and close the game after
                emit("game_over", "Winner is " + winner, broadcast=True, to=game_id)

                # save game
                black_player = Player.query.filter_by(email=current_game.black_player).first().id if current_game.black_player else None
                white_player = Player.query.filter_by(email=current_game.white_player).first().id if current_game.white_player else None
                winner = white_player if is_white_turn else black_player
                # TODO: decide on a computer id value that won't actually be used or save only player games
                saved_game = SavedGame(black_player=black_player, white_player=white_player, winner=winner, game_history=str(current_game.board.board_states))
                db.session.add(saved_game)
                db.session.commit()
                # TODO: maybe get a better format of game_history so that we can easily read it in for training

        else:
            emit("message", "Invalid move " + move_str, to=game_id)
