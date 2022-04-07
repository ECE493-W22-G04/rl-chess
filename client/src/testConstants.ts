import { Game, Leaderboard } from './types';

export const mockCurrentUser = 'bob@gmail.com';

export const mockGame: Game = {
    id: 'asdf-asdf-asdf',
    white_player: null,
    black_player: null,
    host: mockCurrentUser,
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
        email: mockCurrentUser,
        numGamesWon: 10,
        numGamesPlayed: 12,
        winRate: 0.8333333333333334,
    },
    {
        email: 'alice@gmail.com',
        numGamesWon: 9,
        numGamesPlayed: 13,
        winRate: 0.6923076923076923,
    },
];
