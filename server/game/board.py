from .piece import Piece
from .move import Move
from .validators import is_diagonal_forward, is_same_side, is_diagonal_move, is_forward_move, is_pawns_first_move, is_diagonal_path_clear, is_knight_move, is_rook_move, is_rook_path_clear
from .actions import ACTIONS
from copy import deepcopy
import json


class Board:

    def __init__(self) -> None:
        back_row = [Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK]
        front_row = [Piece.PAWN] * 8

        self.state = [
            [piece * -1 for piece in back_row],  # Black
            [piece * -1 for piece in front_row],
            [Piece.NONE] * 8,
            [Piece.NONE] * 8,
            [Piece.NONE] * 8,
            [Piece.NONE] * 8,
            [piece for piece in front_row],
            [piece for piece in back_row],  # White
        ]

        self.is_white_turn = True

    def __str__(self) -> str:

        def piece_to_str(piece: int):
            pieces = {
                Piece.NONE: ' ',
                Piece.ROOK: '♜',
                Piece.KNIGHT: '♞',
                Piece.BISHOP: '♝',
                Piece.QUEEN: '♛',
                Piece.KING: '♚',
                Piece.PAWN: '♟',
            }
            black_to_white_offset = ord('♖') - ord('♜')
            offset = 0 if piece < 0 else black_to_white_offset
            return chr(ord(pieces[abs(piece)]) + offset)

        return '\n\n'.join(['\t'.join([piece_to_str(piece) for piece in row]) for row in self.state])

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def get_actions(self):
        return ACTIONS

    def get_legal_actions(self) -> list[Move]:
        """Returns a subset of possible actions such that none of the actions result in a check"""
        legal_actions = []
        for action in self.get_possible_actions():
            new_state = deepcopy(self)
            new_state.__register_move_unsafe(action)
            new_state.is_white_turn = self.is_white_turn
            if new_state.is_check():
                continue
            legal_actions.append(action)
        return legal_actions

    def get_possible_actions(self):
        legal_actions: list[Move] = []
        for move in ACTIONS:
            if not self.is_move_possible(move):
                continue
            legal_actions.append(move)
        return legal_actions

    def is_check(self) -> bool:
        """Returns true if the current player is being checked"""
        was_white_turn = self.is_white_turn

        # See if opponent has a move that can capture a king
        self.is_white_turn = not self.is_white_turn
        possible_actions = self.get_possible_actions()

        for action in possible_actions:
            target_piece = self.state[action.to_square.y][action.to_square.x]
            if abs(target_piece) == Piece.KING:
                self.is_white_turn = was_white_turn
                return True

        self.is_white_turn = was_white_turn
        return False

    def is_checkmate(self) -> bool:
        """Returns true if the current player is being checkmated"""
        if not self.is_check():
            return False

        legal_actions = self.get_legal_actions()
        can_king_move = False
        for legal_action in legal_actions:
            from_piece = self.state[legal_action.from_square.y][legal_action.from_square.x]
            if abs(from_piece) == Piece.KING:
                can_king_move = True
                break

        return not can_king_move

    def __register_move_unsafe(self, move: Move) -> bool:
        """Registers move without validation"""
        piece_to_move = self.state[move.from_square.y][move.from_square.x]
        self.state[move.to_square.y][move.to_square.x] = piece_to_move
        self.state[move.from_square.y][move.from_square.x] = Piece.NONE

        self.is_white_turn = not self.is_white_turn
        return True

    def register_move(self, move: Move) -> bool:
        if not self.validate_move(move):
            return False

        return self.__register_move_unsafe(move)

    def is_move_possible(self, move: Move):
        from_x = move.from_square.x
        from_y = move.from_square.y
        to_x = move.to_square.x
        to_y = move.to_square.y

        for coordinate in [from_x, from_y, to_x, to_y]:
            if coordinate < 0 or coordinate > 7:
                return False

        piece_to_move = self.state[from_y][from_x]
        piece_at_target = self.state[to_y][to_x]

        if self.is_white_turn and piece_to_move < 0:
            return False

        if not self.is_white_turn and piece_to_move > 0:
            return False

        if to_x == from_x and to_y == from_y:
            return False

        if is_same_side(piece_to_move, piece_at_target):
            return False

        if abs(piece_to_move) == Piece.PAWN:
            if is_diagonal_forward(move, piece_to_move > 0):
                return abs(to_x - from_x) == 1 and abs(to_y - from_y) == 1 and piece_at_target != Piece.NONE
            if is_pawns_first_move(move, piece_to_move > 0):
                return is_forward_move(move, piece_to_move > 0) and abs(to_y - from_y) <= 2
            return is_forward_move(move, piece_to_move > 0) and abs(to_y - from_y) == 1
        if abs(piece_to_move) == Piece.BISHOP:
            return is_diagonal_move(move) and is_diagonal_path_clear(self.state, move)
        if abs(piece_to_move) == Piece.KNIGHT:
            return is_knight_move(move)
        if abs(piece_to_move) == Piece.ROOK:
            return is_rook_move(move) and is_rook_path_clear(self.state, move)
        if abs(piece_to_move) == Piece.QUEEN:
            return (is_diagonal_move(move) and is_diagonal_path_clear(self.state, move)) or (is_rook_move(move) and is_rook_path_clear(self.state, move))
        if abs(piece_to_move) == Piece.KING:
            return abs(to_x - from_x) <= 1 and abs(to_y - from_y) <= 1

        return False

    def validate_move(self, move: Move) -> bool:
        return self.is_move_possible(move) and move in self.get_legal_actions()
