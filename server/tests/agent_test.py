from server.rl_agent.agent import RlAgent
from server.game.board import Board


def test_rl_can_predict_moves():
    rl_agent = RlAgent()
    board = Board()
    for i in range(5):
        action = rl_agent.predict(board)
        assert board.register_move(action)
