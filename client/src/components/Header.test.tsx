import React from 'react';
import { shallow } from 'enzyme';
import { io } from 'socket.io-client';
import { BrowserRouter, Link } from 'react-router-dom';
import { render } from '@testing-library/react';

import Header from './Header';
import socket from '../services/socket';
import AuthService from '../services/auth';
import { mockCurrentUser } from '../testConstants';

jest.mock('../services/socket');
const mockSocket = jest.mocked(socket);

jest.mock('socket.io-client');
const mockedIo = jest.mocked(io);
mockedIo.mockReturnValue(mockSocket);

jest.mock('../services/auth');
const mockedAuthService = jest.mocked(AuthService);

jest.mock('../services/auth');
jest.mocked(AuthService);

beforeEach(() => {
    mockedAuthService.getCurrentUser.mockReturnValue(mockCurrentUser);
});

test('contains RL chess', () => {
    const resp = shallow(<Header />);
    const link = resp.find(Link).first();
    expect(link.text()).toBe('RL Chess');
});

test('contains does not contain link to leaderboard when not authenticated', async () => {
    mockedAuthService.getCurrentUser.mockReturnValue(null);
    const resp = render(
        <BrowserRouter>
            <Header />
        </BrowserRouter>
    );

    try {
        await resp.findByText('Leaderboard');
    } catch (err) {
        return;
    }
    fail('Can still see Leaderboard link even when not authenticated');
});

test('contains link to leaderboard when authenticated', async () => {
    const resp = render(
        <BrowserRouter>
            <Header />
        </BrowserRouter>
    );

    const leaderboardLink = await resp.findByText('Leaderboard');
    expect(leaderboardLink).not.toBeNull();
});
