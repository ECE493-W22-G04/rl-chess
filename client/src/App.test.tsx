import React from 'react';
import App from './App';
import { shallow } from 'enzyme';
import { Link } from 'react-router-dom';

test('renders RL Chess homepage', () => {
    const resp = shallow(<App />);
    const link = resp.find(Link);
    expect(link.text).toBe('RL Chess');
});

test('contains logo', () => {
    const res = shallow(<App />);
    const imageNode = res.find('img');

    expect(imageNode.prop('alt')).toBe('logo');
});
