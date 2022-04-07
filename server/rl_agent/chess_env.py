import numpy as np
from gym import Env, spaces

from server.game.board import Board

# This File is used to satisfy the following functional requirements:
# FR6 - Computer.Move


class ChessEnv(Env):

    def __init__(self):
        super(ChessEnv, self).__init__()

        self.__state = Board()

        self.observation_shape = (8, 8)
        self.observation_space = spaces.Box(low=np.ones(self.observation_shape) * -8, high=np.ones(self.observation_shape) * 8, dtype=np.int32)

        self.action_space = spaces.Discrete(len(self.__state.get_actions()))

    def reset(self):
        self.__state = Board()
        return self.__state.state

    def step(self, action):
        done = False

        if self.__state.register_move(self.__state.get_actions()[action]):
            reward = 1
        else:
            reward = -1

        if self.__state.is_checkmate():
            reward = 1000
            done = True

        if self.__state.is_draw():
            reward = 100
            done = True

        return self.__state.state, reward, done, {}

    def render(self, mode="human"):
        pass
