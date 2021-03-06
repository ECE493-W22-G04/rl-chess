from .piece import Piece
from .move import Move, Square
from .validators import is_diagonal_forward, is_same_side, is_diagonal_move, is_forward_move, is_pawns_first_move, is_diagonal_path_clear, is_knight_move, is_rook_move, is_rook_path_clear, is_pawn_path_clear, is_pawn_end_row_valid
from .actions import ACTIONS
from copy import deepcopy
from collections import Counter
import json
import itertools

# This File is used to satisfy the following functional requirements:
# FR18 - Alternate.Turns
# FR19 - Detect.Stalemate
# FR20 - Valid.Move
# FR22 - Detect.Checkmate
# FR23 - Detect.Repetition


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
        self.moves: list[Move] = []
        self.board_states = [deepcopy(self.state)]
        self.last_move: Move = None
        self.fifty_move_count = 0

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
        return self.__dict__

    def get_actions(self):
        return ACTIONS

    def get_legal_actions(self) -> list[Move]:
        """Returns a subset of possible actions such that none of the actions result in a check"""
        return [ACTIONS[i] for i in self.get_legal_action_indices()]

    def get_legal_action_indices(self) -> list[Move]:
        """Returns the indices of the subset of possible actions such that none of the actions result in a check"""
        legal_actions = []
        possible_actions = self.get_possible_action_indices()
        for i in possible_actions:
            new_state = deepcopy(self)
            new_state.__register_move_unsafe(ACTIONS[i])
            new_state.is_white_turn = self.is_white_turn
            if new_state.is_check():
                continue
            legal_actions.append(i)
        return legal_actions

    def get_possible_actions(self):
        return [ACTIONS[i] for i in self.get_possible_action_indices()]

    def get_possible_action_indices(self):
        legal_actions: list[int] = []
        for i, move in enumerate(ACTIONS):
            if not self.is_move_possible(move):
                continue
            legal_actions.append(i)
        return legal_actions

    def is_draw(self) -> bool:
        if self.is_stalemate():
            return True

        if self.is_threefold_repetition():
            return True

        if self.is_fifty_move_rule():
            return True
        return False

    def is_stalemate(self) -> bool:
        return len(self.get_legal_actions()) == 0

    def is_threefold_repetition(self) -> bool:
        mapped_states = map(lambda x: str(x), self.board_states)
        counts = dict(Counter(mapped_states))
        return len(list(filter(lambda x: x >= 3, counts.values()))) > 0

    def is_fifty_move_rule(self) -> bool:
        if self.fifty_move_count >= 100:  # double because a move is a white and black move
            return True
        return False

    def is_attacked(self, attack_square: Square):
        multiplier = -1 if self.is_white_turn else 1

        for (from_x, from_y) in itertools.product(range(8), repeat=2):
            piece = self.state[from_y][from_x]

            # only opposite sided pieces attack
            if (piece * multiplier) <= 0:
                continue

            move = Move(Square(from_x, from_y), attack_square)
            x_diff = abs(from_x - attack_square.x)
            y_diff = abs(from_y - attack_square.y)

            if abs(piece) == Piece.PAWN:
                modifier = -1 if piece > 0 else 1
                # attack diagonally
                return (from_y + modifier) == attack_square.y and x_diff == 1
            elif abs(piece) == Piece.BISHOP:
                if is_diagonal_path_clear(self.state, move):
                    return True
            elif abs(piece) == Piece.KNIGHT:
                if (x_diff == 2 and y_diff == 1) or (x_diff == 1 and y_diff == 2):
                    return True
            elif abs(piece) == Piece.ROOK:
                if is_rook_path_clear(self.state, move):
                    return True
            elif abs(piece) == Piece.QUEEN:
                if is_rook_path_clear(self.state, move) and is_diagonal_path_clear(self.state, move):
                    return True
            elif abs(piece) == Piece.KING:
                if x_diff <= 1 and y_diff <= 1:
                    return True
        return False

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

        # find king
        king_piece = Piece.KING if self.is_white_turn else -Piece.KING

        king_square = None
        for (check_x, check_y) in itertools.product(range(8), repeat=2):
            if self.state[check_y][check_x] == king_piece:
                king_square = Square(check_x, check_y)
                break

        # can only occur in testing, don't want to break
        if king_square is None:
            return False

        legal_actions = self.get_legal_actions()
        can_king_move = False
        can_block = False
        for legal_action in legal_actions:
            from_piece = self.state[legal_action.from_square.y][legal_action.from_square.x]
            if abs(from_piece) == Piece.KING:
                can_king_move = True
                break
            # simulate move
            sim_board = deepcopy(self)
            sim_board.__register_move_unsafe(legal_action)
            sim_board.is_white_turn = self.is_white_turn
            if not sim_board.is_attacked(king_square):
                can_block = True
                break

        return not (can_king_move or can_block)

    def __register_move_unsafe(self, move: Move) -> bool:
        """Registers move without validation"""
        piece_to_move = self.state[move.from_square.y][move.from_square.x]
        piece_to_capture = self.state[move.to_square.y][move.to_square.x]

        if abs(piece_to_move) == Piece.PAWN or piece_to_capture != Piece.NONE:
            self.fifty_move_count = 0
        else:
            self.fifty_move_count += 1

        # castling
        if self.is_valid_castle(move):
            # move the king
            self.state[move.to_square.y][move.to_square.x] = piece_to_move
            self.state[move.from_square.y][move.from_square.x] = Piece.NONE

            # move the rook
            if move.to_square.x == 2:
                piece_to_move = self.state[move.from_square.y][0]
                self.state[move.from_square.y][3] = piece_to_move
                self.state[move.from_square.y][0] = Piece.NONE
            else:
                piece_to_move = self.state[move.from_square.y][7]
                self.state[move.from_square.y][5] = piece_to_move
                self.state[move.from_square.y][7] = Piece.NONE
        elif self.is_en_passant(move):
            # move the pawn
            self.state[move.to_square.y][move.to_square.x] = piece_to_move
            self.state[move.from_square.y][move.from_square.x] = Piece.NONE

            # capture the other pawn
            self.state[self.last_move.to_square.y][self.last_move.to_square.x] = Piece.NONE

        # promotion
        elif is_pawn_end_row_valid(move, piece_to_move) and move.promotion != None:
            multiplier = 1 if self.is_white_turn else -1
            self.state[move.to_square.y][move.to_square.x] = move.promotion * multiplier
            self.state[move.from_square.y][move.from_square.x] = Piece.NONE

        else:
            self.state[move.to_square.y][move.to_square.x] = piece_to_move
            self.state[move.from_square.y][move.from_square.x] = Piece.NONE

        self.is_white_turn = not self.is_white_turn

        self.board_states.append(deepcopy(self.state))
        self.last_move = move
        self.moves.append(move)

        return True

    def register_move(self, move: Move) -> bool:
        if not self.validate_move(move):
            return False

        return self.__register_move_unsafe(move)

    def is_valid_castle(self, move: Move) -> bool:
        from_x = move.from_square.x
        from_y = move.from_square.y
        to_x = move.to_square.x
        to_y = move.to_square.y
        from_piece = self.state[from_y][from_x]

        # not a castling move
        if (not (from_y == 0 or from_y == 7)) or from_y != to_y or from_x != 4 or (not (to_x == 2 or to_x == 6)) or abs(from_piece) != Piece.KING:
            return False

        # check if a piece is in the way
        if from_y == 0:
            if to_x == 2 and (self.state[0][0] != -Piece.ROOK or self.state[0][1] != Piece.NONE or self.state[0][2] != Piece.NONE or self.state[0][3] != Piece.NONE or self.state[0][4] != -Piece.KING):
                return False
            if to_x == 6 and (self.state[0][7] != -Piece.ROOK or self.state[0][6] != Piece.NONE or self.state[0][5] != Piece.NONE or self.state[0][4] != -Piece.KING):
                return False
        else:
            if to_x == 2 and (self.state[7][0] != Piece.ROOK or self.state[7][1] != Piece.NONE or self.state[7][2] != Piece.NONE or self.state[7][3] != Piece.NONE or self.state[7][4] != Piece.KING):
                return False
            if to_x == 6 and (self.state[7][7] != Piece.ROOK or self.state[7][6] != Piece.NONE or self.state[7][5] != Piece.NONE or self.state[7][4] != Piece.KING):
                return False

        white_rook_0_moved = False
        white_rook_7_moved = False
        white_king_moved = False
        black_rook_0_moved = False
        black_rook_7_moved = False
        black_king_moved = False

        # check if previous boardstates moved the king/rook in question
        for state in self.board_states:
            if state[0][0] != -Piece.ROOK:
                black_rook_0_moved = True
            if state[0][4] != -Piece.KING:
                black_king_moved = True
            if state[0][7] != -Piece.ROOK:
                black_rook_7_moved = True

            if state[7][0] != Piece.ROOK:
                white_rook_0_moved = True
            if state[7][4] != Piece.KING:
                white_king_moved = True
            if state[7][7] != Piece.ROOK:
                white_rook_7_moved = True

        if from_y == 0:
            if black_king_moved:
                return False
            if to_x == 2 and black_rook_0_moved:
                return False
            if to_x == 6 and black_rook_7_moved:
                return False
        else:
            if white_king_moved:
                return False
            if to_x == 2 and white_rook_0_moved:
                return False
            if to_x == 6 and white_rook_7_moved:
                return False

        # check if king would be attacked
        if from_y == 0:
            if to_x == 2:
                if self.is_attacked(Square(3, 0)) or self.is_attacked(Square(2, 0)):
                    return False
            else:
                if self.is_attacked(Square(5, 0)) or self.is_attacked(Square(6, 0)):
                    return False
        else:
            if to_x == 2:
                if self.is_attacked(Square(3, 7)) or self.is_attacked(Square(2, 7)):
                    return False
            else:
                if self.is_attacked(Square(5, 7)) or self.is_attacked(Square(6, 7)):
                    return False

        # cannot castle while in check
        if self.is_attacked(move.from_square):
            return False

        return True

    def is_en_passant(self, move: Move):
        if self.last_move is None:
            return False
        piece_to_move = self.state[move.from_square.y][move.from_square.x]
        if not is_diagonal_forward(move, piece_to_move > 0):
            return False

        # prevent bishop like moves
        if abs(move.from_square.y - move.to_square.y) != 1 or abs(move.from_square.x - move.to_square.x) != 1:
            return False

        # last move was a double move
        last_piece_moved = self.state[self.last_move.to_square.y][self.last_move.to_square.x]
        x_diff = self.last_move.from_square.x - self.last_move.to_square.x
        y_diff = self.last_move.from_square.y - self.last_move.to_square.y
        if abs(piece_to_move) != Piece.PAWN or abs(last_piece_moved) != Piece.PAWN or x_diff != 0 or abs(y_diff) != 2:
            return False

        test_y = 2 if piece_to_move > 0 else 5

        # current move captures
        return move.to_square.x == self.last_move.from_square.x and move.to_square.y == test_y

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

        if abs(piece_to_move) != Piece.PAWN and move.promotion != None:
            return False

        if abs(piece_to_move) == Piece.PAWN:
            if is_diagonal_forward(move, piece_to_move > 0):
                return self.is_en_passant(move) or (abs(to_x - from_x) == 1 and abs(to_y - from_y) == 1 and piece_at_target != Piece.NONE and is_pawn_end_row_valid(move, piece_to_move))
            if is_pawns_first_move(move, piece_to_move > 0):
                return is_forward_move(move, piece_to_move > 0) and abs(to_y - from_y) <= 2 and is_pawn_path_clear(self.state, move, piece_to_move > 0)
            return is_forward_move(move, piece_to_move > 0) and abs(to_y - from_y) == 1 and is_pawn_path_clear(self.state, move, piece_to_move > 0) and is_pawn_end_row_valid(move, piece_to_move)
        if abs(piece_to_move) == Piece.BISHOP:
            return is_diagonal_move(move) and is_diagonal_path_clear(self.state, move)
        if abs(piece_to_move) == Piece.KNIGHT:
            return is_knight_move(move)
        if abs(piece_to_move) == Piece.ROOK:
            return is_rook_move(move) and is_rook_path_clear(self.state, move)
        if abs(piece_to_move) == Piece.QUEEN:
            return (is_diagonal_move(move) and is_diagonal_path_clear(self.state, move)) or (is_rook_move(move) and is_rook_path_clear(self.state, move))
        if abs(piece_to_move) == Piece.KING:
            return (abs(to_x - from_x) <= 1 and abs(to_y - from_y) <= 1) or self.is_valid_castle(move)

        return False

    def validate_move(self, move: Move) -> bool:
        return self.is_move_possible(move) and move in self.get_legal_actions()
