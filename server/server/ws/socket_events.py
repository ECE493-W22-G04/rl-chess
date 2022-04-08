import json
from flask import request
from flask_socketio import SocketIO, join_room, emit, send
import eventlet

from rl_agent import rl_agent
from server.game.move import Move, Square
from server.api.routes.games import current_games
from server.api.models import SavedGame, Player, Game, db

PLAYERS_PER_PVP_ROOM = 2
PLAYERS_PER_PVC_ROOM = 1

user_rooms: dict[str, list[str]] = {}
socket_id_to_user: dict[str, str] = {}
user_to_room: dict[str, str] = {}

# This File is used to satisfy the following functional requirements:
# FR7 - Computer.Model
# FR16 - Start.Game
# FR24 - Record.Game
# FR26 - Accept.Draw
# FR27 - Store.Draw
# FR29 - Leave.Game


def register_ws_events(socketio: SocketIO):

    @socketio.on("connect")
    def connect():
        pass

    @socketio.on("disconnect")
    def disconnect():
        user = socket_id_to_user.get(request.sid)
        if user == None:
            # User never made it into a room
            return
        del socket_id_to_user[request.sid]

        game_id = user_to_room.get(user)
        if game_id == None or (game_id not in current_games) or (game_id not in user_rooms):
            # Game was never created
            return
        del user_to_room[user]

        game = current_games[game_id]
        players_in_room = user_rooms[game_id]
        players_in_room.remove(user)

        if not game.has_started:
            # Give chance for host to reinvite client
            emit('room_not_full', broadcast=True, to=game_id)
            emit('players_in_room', players_in_room, broadcast=True, to=game_id)
        else:
            # Wrap up current game
            winner = players_in_room[0] if len(players_in_room) > 0 else None
            payload = {'winner': winner}
            emit('game_over', json.dumps(payload), broadcast=True, to=game.id)
            save_game(current_games[game_id], is_draw=False)

        if len(players_in_room) != 0:
            return

        # No more users in ther oom
        del user_rooms[game_id]
        del current_games[game_id]

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

        socket_id_to_user[request.sid] = user
        user_to_room[user] = game_id

        join_room(game_id)
        emit('players_in_room', user_rooms[game_id], broadcast=True, to=game_id)

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

        other_user = get_other_player(game_id, user)

        game = current_games[game_id]
        # check if player in room and is host of current game
        if user in user_rooms[game_id] and user == game.host:
            if color == "white":
                game.set_white_player(user)
                if game.is_pvp:
                    game.set_black_player(other_user)
            elif color == "black":
                game.set_black_player(user)
                if game.is_pvp:
                    game.set_white_player(other_user)

        game.start_game()
        emit('update', game.toJSON(), broadcast=True, to=game_id)
        eventlet.sleep(0)

        # Make first move as computer
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
        # if no promotion, expects this to be 0
        promotion = data["promotion"]

        # check game exists
        if game_id not in current_games:
            emit("message", "Attempted to make move with invalid game id " + game_id, broadcast=True, to=game_id)
            return

        # check if move is valid
        (move_from, move_to) = move_str.split("->")
        (from_x, from_y) = move_from.split(",")
        (to_x, to_y) = move_to.split(",")
        if int(promotion) != 0:
            move = Move(Square(int(from_x), int(from_y)), Square(int(to_x), int(to_y)), int(promotion))
        else:
            move = Move(Square(int(from_x), int(from_y)), Square(int(to_x), int(to_y)))
        game = current_games[game_id]
        if not game.board.register_move(move):
            emit("message", "Invalid move")
            return
        emit('update', game.toJSON(), broadcast=True, to=game_id)
        eventlet.sleep(0)

        if game.board.is_checkmate():
            handle_game_over(game)
            return

        if game.board.is_draw():
            payload = {'winner': 'Nobody'}
            emit("game_over", json.dumps(payload), broadcast=True, to=game_id)
            save_game(game, True)
            # TODO: remove game from current_games
            return

        # Make computer move
        if game.is_pvp:
            return
        rl_move = rl_agent.predict(game.board)
        game.board.register_move(rl_move)
        emit('update', game.toJSON(), broadcast=True, to=game_id)

        if game.board.is_checkmate():
            handle_game_over(game)

    @socketio.on("offer_draw")
    def offer_draw(data):
        game_id = data["gameId"]
        current_player = data["currentPlayer"]
        other_player = get_other_player(game_id, current_player)

        data = {'offer_draw_to': other_player}
        emit('offer_draw', json.dumps(data), broadcast=True, to=game_id)

    @socketio.on("accept_draw")
    def accept_draw(data):
        game_id = data["gameId"]
        payload = {'winner': 'Nobody'}
        emit('game_over', json.dumps(payload), broadcast=True, to=game_id)
        save_game(current_games[game_id], True)

    @socketio.on("concede")
    def concede(data):
        game_id = data["gameId"]
        current_player = data["currentPlayer"]
        other_player = get_other_player(game_id, current_player)
        winner = other_player if current_games[game_id].is_pvp else 'RL Agent'
        payload = {'winner': winner}
        emit('game_over', json.dumps(payload), broadcast=True, to=game_id)
        save_game(current_games[game_id], False)


def get_other_player(game_id, user):
    for user_in_room in user_rooms[game_id]:
        if user_in_room != user:
            return user_in_room
    return ""


def handle_game_over(game: Game):
    winner = game.white_player
    if game.board.is_white_turn:
        # Black player made the last move and was a checkmate
        winner = game.black_player
    if not game.is_pvp and winner == '':
        winner = 'RL Agent'
    payload = {'winner': winner}
    emit('game_over', json.dumps(payload), broadcast=True, to=game.id)
    save_game(game, False)


def save_game(game: Game, is_draw: bool):
    is_white_turn = not game.board.is_white_turn  # opposite because it registered move

    black_player = Player.query.filter_by(email=game.black_player).first().id if game.black_player else None
    white_player = Player.query.filter_by(email=game.white_player).first().id if game.white_player else None
    if is_draw:
        winner = None
    else:
        winner = white_player if is_white_turn else black_player
    saved_game = SavedGame(black_player=black_player, white_player=white_player, winner=winner, game_history=json.dumps(game.board.moves), is_pvp=game.is_pvp)
    db.session.add(saved_game)
    db.session.commit()
