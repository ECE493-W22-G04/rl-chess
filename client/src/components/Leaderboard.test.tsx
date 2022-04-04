import React from 'react';
import { shallow } from 'enzyme';

import Leaderboard from './Leaderboard';
import { getLeaderboard } from '../services/leaderboard';
import { mockLeaderboard } from '../testConstants';
import { render } from '@testing-library/react';

jest.mock('../services/leaderboard');
const mockGetLeaderboard = jest.mocked(getLeaderboard, true);

beforeEach(() => {
    mockGetLeaderboard.mockResolvedValueOnce(mockLeaderboard);
});

test('renders loading screen initially', () => {
    const res = shallow(<Leaderboard />);
    expect(res.find(<p>Loading...</p>)).not.toBeNull();
});

test('calls getLeaderboard', async () => {
    const res = render(<Leaderboard />);
    await res.findByText('Rank');
    expect(mockGetLeaderboard).toBeCalledTimes(1);
});

test('has entries for all ranked users', async () => {
    const res = render(<Leaderboard />);
    for (const entry of mockLeaderboard) {
        const entryDom = await res.findByText(entry.email);
        expect(entryDom).not.toBeNull();
    }
});
