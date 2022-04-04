import { Game, Leaderboard } from './types';

export const mockGame: Game = {
    id: 'asdf-asdf-asdf',
    white_player: null,
    black_player: null,
    host: 'bob@gmail.com',
    board: {
        state: [
            [-4, -3, -2, -5, -6, -2, -3, -4],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [4, 3, 2, 5, 6, 2, 3, 4],
        ],
        is_white_turn: true,
        moves: [],
    },
    has_started: true,
};

export const mockLeaderboard: Leaderboard = [
    {
        email: 'bob@gmail.com',
        numWins: 2,
    },
    {
        email: 'alice@gmail.com',
        numWins: 1,
    },
];
