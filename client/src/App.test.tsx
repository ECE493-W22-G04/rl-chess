import React from 'react';
import App from './App';
import { shallow } from 'enzyme';
import socket from './services/socket';
import { io } from 'socket.io-client';
import Header from './components/Header';
import Home from './components/home';

jest.mock('./services/socket');
const mockSocket = jest.mocked(socket);

jest.mock('socket.io-client');
const mockedIo = jest.mocked(io);
mockedIo.mockReturnValue(mockSocket);

test('renders RL Chess homepage', () => {
    const res = shallow(<App />);
    const home = res.find(<Home />);
    expect(home).not.toBeNull();
});

test('contains Header', () => {
    const res = shallow(<App />);
    const header = res.find(<Header />);
    expect(header).not.toBeNull();
});
