import axios from 'axios';
import config from '../config';
import authHeader from './auth-header';
import { createGame, getGameDetails } from './game';
import { Game } from '../types';

jest.mock('axios');
const mockAxios = jest.mocked(axios, true);

jest.mock('./auth-header');
const mockAuthHeader = jest.mocked(authHeader, true);

const API_URL = `${config.SERVER_ENDPOINT}/api/games/`;

const mockGame: Game = {
    id: 'asdf-asdf-asdf',
    whitePlayer: null,
    blackPlayer: null,
    host: 'bob@gmail.com',
    board: {
        state: [
            [-4, -3, -2, -5, -6, -2, -3, -4],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [4, 3, 2, 5, 6, 2, 3, 4],
        ],
        isWhiteTurn: true,
    },
};

describe('createGame', () => {
    const mockPost = jest.fn();

    mockAuthHeader.mockReturnValue({ Authorization: 'Bearer asdfasdf' });

    beforeEach(() => {
        mockAxios.post = mockPost;

        mockPost.mockResolvedValue({
            data: mockGame,
        });
    });

    it(`calls ${API_URL}`, async () => {
        await createGame(false);
        expect(mockAuthHeader).toBeCalledTimes(1);
        expect(mockPost).toBeCalledWith(API_URL, expect.anything(), { headers: mockAuthHeader() });
    });
});

describe('getGameDetails', () => {
    const mockGet = jest.fn();

    mockAuthHeader.mockReturnValue({ Authorization: 'Bearer asdfasdf' });

    beforeEach(() => {
        mockAxios.get = mockGet;
        mockGet.mockResolvedValue({
            data: mockGame,
        });
    });

    it(`calls ${API_URL}{gameId}`, async () => {
        const gameId = 'asdf-asdf-asdf';
        await getGameDetails(gameId);
        expect(mockAuthHeader).toBeCalledTimes(1);
        expect(mockGet).toBeCalledWith(`${API_URL}${gameId}`, { headers: mockAuthHeader() });
    });
});
