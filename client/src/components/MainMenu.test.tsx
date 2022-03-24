import React from 'react';
import { shallow } from 'enzyme';
import { createGame } from '../services/game';
import MainMenu from './MainMenu';
import { mockGame } from '../testConstants';

jest.mock('../services/game');
const mockCreateGame = jest.mocked(createGame, true);

const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
    ...jest.requireActual('react-router-dom'),
    useNavigate: () => mockNavigate,
}));

beforeEach(() => {
    mockCreateGame.mockResolvedValueOnce(mockGame);
});

type OnClickHandler = () => Promise<void>;

test('pvc calls correct handler', async () => {
    const res = shallow(<MainMenu />);

    const onClickHandler = res.find('#pvc').prop('onClick') as unknown as OnClickHandler;
    await onClickHandler();
    expect(mockCreateGame).toBeCalledWith(false);
    expect(mockNavigate).toBeCalledWith(`/game/${mockGame.id}`);
});

test('pvp calls correct handler', async () => {
    const res = shallow(<MainMenu />);

    const onClickHandler = res.find('#pvp').prop('onClick') as unknown as OnClickHandler;
    await onClickHandler();
    expect(mockCreateGame).toBeCalledWith(true);
    expect(mockNavigate).toBeCalledWith(`/game/${mockGame.id}`);
});
