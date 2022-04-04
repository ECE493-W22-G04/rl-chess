import sys
import os

from server.game.board import Board
from rl_agent.agent import RlAgent

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_rl_can_predict_moves():
    rl_agent = RlAgent()
    board = Board()
    for i in range(2):
        action = rl_agent.predict(board)
        assert board.register_move(action)
