import React from 'react';
import App from './App';
import { shallow } from 'enzyme';

test('renders learn react link', () => {
    const res = shallow(<App />);
    expect(res.find('a').text()).toContain('Learn React');
});

test('contains logo', () => {
    const res = shallow(<App />);
    const imageNode = res.find('img');

    expect(imageNode.prop('alt')).toBe('logo');
});
