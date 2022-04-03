import numpy as np

from gym import Env, spaces

from server.game.board import Board


class ChessEnv(Env):

    def __init__(self):
        super(ChessEnv, self).__init__()

        self.__state = Board()

        self.observation_shape = (8, 8)
        self.observation_space = spaces.Box(low=np.zeros(self.observation_shape), high=np.ones(self.observation_shape) * 8, dtype=np.int32)

        self.action_space = spaces.Discrete(len(self.__state.get_actions()))

    def reset(self):
        self.__state = Board()

        return self.__state.state

    def step(self, opponent_move):
        done = False

        if not self.__state.register_move(self.__state.get_actions()[opponent_move]):
            done = True
            reward = -999

            return self.__state.state, reward, done, {}

        opponent_move = np.random.choice(np.array(self.__state.get_legal_action_indices()))
        self.__state.register_move(self.__state.get_actions()[opponent_move])

        reward = 1
        if self.__state.is_checkmate():
            reward = 100
            done = True

        return self.__state.state, reward, done, {}

    def render(self, mode="human"):
        pass
