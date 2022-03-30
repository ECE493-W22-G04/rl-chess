from sys import stderr
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten
from tensorflow.keras.optimizers import Adam
from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

from server.rl_agent.chess_env import ChessEnv
from server.game.board import Board
from server.game.move import Move


class RlAgent():
    WEIGHTS_FILE = 'checkpoints/checkpoint'

    def __init__(self) -> None:
        self.__agent = self.__build_agent()
        self.__load_weights()

    def __build_agent(self) -> DQNAgent:
        env = ChessEnv()
        nb_actions = env.action_space.n

        model = Sequential()
        model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
        model.add(Dense(16))
        model.add(Activation('relu'))
        model.add(Dense(16))
        model.add(Activation('relu'))
        model.add(Dense(16))
        model.add(Activation('relu'))
        model.add(Dense(nb_actions))
        model.add(Activation('linear'))

        memory = SequentialMemory(limit=50000, window_length=1)
        policy = BoltzmannQPolicy()
        dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=50, target_model_update=1e-2, policy=policy)
        dqn.compile(Adam(learning_rate=1e-1), metrics=['mae'])
        return dqn

    def __load_weights(self):
        try:
            self.__agent.load_weights(self.WEIGHTS_FILE)
        except Exception as err:
            print('Could not find weights file, initializing new one', file=stderr)
            self.train(100)

    def predict(self, board: Board) -> Move:
        random_action_index = self.__agent.forward(board.state)
        predicted_move = board.get_actions()[random_action_index]
        if predicted_move in board.get_legal_actions():
            print(f'Agent provided illegal move {predicted_move}', file=stderr)
            return board.get_actions()[random_action_index]

        random_action_index = np.random.choice(board.get_legal_action_indices())
        return board.get_actions()[random_action_index]

    def train(self, num_episodes: int = 50000):
        env = ChessEnv()
        self.__agent.fit(env, nb_steps=num_episodes, visualize=False, verbose=1)
        self.__agent.save_weights(self.WEIGHTS_FILE, overwrite=True)
