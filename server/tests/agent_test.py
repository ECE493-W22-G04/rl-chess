import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ..rl_agent.agent import RlAgent
from ..game.board import Board



def test_rl_can_predict_moves():
    rl_agent = RlAgent()
    board = Board()
    for i in range(3):
        action = rl_agent.predict(board)
        assert board.register_move(action)
