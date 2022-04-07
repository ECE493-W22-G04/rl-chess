import os
from random import random
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
        dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=50, target_model_update=1e-2, policy=policy, test_policy=policy)
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

    def train(self, num_episodes: int = 1000):
        # learn on random move games
        env = ChessEnv()
        self.__agent.fit(env, nb_steps=num_episodes, visualize=False, verbose=1)
        self.__agent.save_weights(self.WEIGHTS_FILE, overwrite=True)

    def belief_revision(self, num_episodes: int = 10):
        env = ChessEnv()
        trained_id = 0

        try:
            f = open("revised.txt", "r")
            trained_id = int(f.readline())
        except:
            print("creating a record of games trained")

        games = None
        app = create_app()
        app.config.update({"SQLALCHEMY_DATABASE_URI": os.getenv('GAMES_DATABASE_URL').replace("postgres://", "postgresql://", 1)})
        with app.app_context():
            games = SavedGame.query.filter(SavedGame.id > trained_id).all()

        if games is None:
            return

        for game in games:
            self.__load_weights()
            moves = json.loads(game.game_history)
            moves = list(map(lambda move: Move(Square(move[0][0], move[0][1]), Square(move[1][0], move[1][1]), move[2]), moves))

            # play game and check that state doesn't repeat initial board position
            test_board = Board()
            flag = 0
            while True:
                for (i, move) in enumerate(moves):
                    test_board.register_move(move)
                    if test_board.state == Board().state:
                        flag = i
                        break
                if flag != 0:
                    moves = moves[(i + 1):]  # remove the repeating moves from the array
                else:
                    break

            print(f"training game {game.id}")

            env.reset()
            index = 0

            def train_policy(observation):
                nonlocal index
                if observation == Board().state:
                    index = 0
                move = moves[index]
                index += 1
                return ACTIONS.index(move)

            for _ in range(num_episodes):
                self.__agent.fit(env, nb_steps=100, visualize=False, start_step_policy=train_policy, nb_max_start_steps=len(moves), verbose=1)
                self.__agent.save_weights(self.WEIGHTS_FILE, overwrite=True)
            trained_id += 1

        with open("revised.txt", "w") as f:
            f.write(str(trained_id))
