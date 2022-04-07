from copy import deepcopy
from sys import stderr
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten
from tensorflow.keras.optimizers import Adam
from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory
from rl_agent.chess_env import ChessEnv
from server.game.board import Board
from server.game.move import Move, Square
from server.api.models import SavedGame
from server.api import create_app
from server.game.actions import ACTIONS
import json

# This File is used to satisfy the following functional requirements:
# FR5 - Computer.Setup
# FR7 - Computer.Model
# FR9 - Computer.Self.Learn


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
        self.__agent = self.__build_agent()
        self.__load_weights()

        actions = board.get_actions()
        predicted_move_index = self.__agent.forward(board.state)
        predicted_move = actions[predicted_move_index]

        if not predicted_move in board.get_legal_actions():
            print(f'Agent provided illegal move {predicted_move}', file=stderr)
            random_action_index = np.random.choice(board.get_legal_action_indices())
            return actions[random_action_index]

        return predicted_move

    def train(self, num_episodes: int = 50000):
        env = ChessEnv()
        self.__agent.fit(env, nb_steps=num_episodes, visualize=False, verbose=1)
        self.__agent.save_weights(self.WEIGHTS_FILE, overwrite=True)

    def belief_revision(self, num_episodes: int = 100):
        env = ChessEnv()
        trained_id = 0

        try:
            f = open("revised.txt", "r")
            trained_id = int(f.readline())
        except:
            print("creating a record of games trained")

        games = None
        app = create_app()
        with app.app_context():
            games = SavedGame.query.filter(SavedGame.id > trained_id).all()

        if games is None:
            return

        for game in games:
            moves = json.loads(game.game_history)
            print("training game ", game.id)

            # fit games 1 at a time since train_policy will not reset
            for _ in range(num_episodes):
                env.reset()
                move_copy = deepcopy(moves)

                def train_policy(observation):
                    move = move_copy.pop(0)
                    action_move = Move(Square(move[0][0], move[0][1]), Square(move[1][0], move[1][1]), move[2])
                    return ACTIONS.index(action_move)

                self.__agent.fit(env, nb_steps=1, visualize=False, start_step_policy=train_policy, nb_max_start_steps=len(moves), verbose=0)

            self.__agent.save_weights(self.WEIGHTS_FILE, overwrite=True)
            trained_id += 1

        with open("revised.txt", "w") as f:
            f.write(str(trained_id))