import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';
import { shallow } from 'enzyme';

test('renders learn react link', () => {
    render(<App />);
    const linkElement = screen.getByText(/learn react/i);
    expect(linkElement).toBeInTheDocument();
});

test('contains logo', () => {
    const res = shallow(<App />);
    const imageNode = res.find('img');

    expect(imageNode.prop('alt')).toBe('logo');
});
