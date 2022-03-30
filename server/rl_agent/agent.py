import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten
from tensorflow.keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

from rl_agent.chess_env import ChessEnv
from game.board import Board
from game.move import Move

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
        self.__agent.load_weights(self.WEIGHTS_FILE)
    
    def predict(self, board: Board) -> Move:
        random_action_index = self.__agent.forward(board.state)
        if board.get_actions()[random_action_index] in board.get_legal_actions():
            return board.get_actions()[random_action_index]
        
        random_action_index = np.random.choice(board.get_legal_action_indices())
        return board.get_actions[random_action_index]

    def train(self):
        env = ChessEnv()
        self.__agent.fit(env, nb_steps=50000, visualize=False, verbose=1)
        self.__agent.save_weights(self.WEIGHTS_FILE, overwrite=True)
