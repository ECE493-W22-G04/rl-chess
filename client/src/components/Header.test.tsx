import React from 'react';
import { shallow } from 'enzyme';
import { io } from 'socket.io-client';
import socket from '../services/socket';
import Header from './Header';
import { Link } from 'react-router-dom';

jest.mock('../services/socket');
const mockSocket = jest.mocked(socket);

jest.mock('socket.io-client');
const mockedIo = jest.mocked(io);
mockedIo.mockReturnValue(mockSocket);

test('contains RL chess', () => {
    const resp = shallow(<Header />);
    const link = resp.find(Link).first();
    expect(link.text()).toBe('RL Chess');
});
