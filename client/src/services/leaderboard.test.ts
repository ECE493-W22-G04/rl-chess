import axios from 'axios';
import config from '../config';
import authHeader from './auth-header';
import { mockLeaderboard } from '../testConstants';
import { getLeaderboard } from './leaderboard';

jest.mock('axios');
const mockAxios = jest.mocked(axios, true);

jest.mock('./auth-header');
const mockAuthHeader = jest.mocked(authHeader, true);

const API_URL = `${config.SERVER_ENDPOINT}/api/leaderboard/`;

describe('getLeaderboard', () => {
    const mockGet = jest.fn();

    mockAuthHeader.mockReturnValue({ Authorization: 'Bearer asdfasdf' });

    beforeEach(() => {
        mockAxios.get = mockGet;

        mockGet.mockResolvedValue({
            data: mockLeaderboard,
        });
    });

    it(`calls ${API_URL}`, async () => {
        await getLeaderboard();
        expect(mockAuthHeader).toBeCalledTimes(1);
        expect(mockGet).toBeCalledWith(API_URL, { headers: mockAuthHeader() });
    });
});
