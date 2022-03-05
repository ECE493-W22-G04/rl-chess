import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders RL Chess homepage', () => {
    render(<App />);
    const linkElement = screen.getByText(/RL Chess/i);
    expect(linkElement).toBeInTheDocument();
});
