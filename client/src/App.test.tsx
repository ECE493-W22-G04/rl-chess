import React from 'react';
import App from './App';
import { shallow } from 'enzyme';
import { Link } from 'react-router-dom';
import socket from './services/socket';
import { io } from 'socket.io-client';

jest.mock('./services/socket');
const mockSocket = jest.mocked(socket);

jest.mock('socket.io-client');
const mockedIo = jest.mocked(io);
mockedIo.mockReturnValue(mockSocket);

test('renders RL Chess homepage', () => {
    const resp = shallow(<App />);
    const link = resp.find(Link).first();
    expect(link.text()).toBe('RL Chess');
});

test('contains logo', () => {
    const res = shallow(<App />);
    const imageNode = res.find('img');
    expect(imageNode.prop('alt')).toBe('logo');
});
