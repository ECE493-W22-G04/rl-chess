import { shallow } from 'enzyme';
import React from 'react';
import Modal from 'react-bootstrap/Modal';

import WinnerModal from './WinnerModal';
import { mockGame } from '../../testConstants';

test('it renders nothing if there is no winner', () => {
    const res = shallow(<WinnerModal winner={null} />);
    expect(res).not.toContain(Modal);
});

test('it shows a modal when there is a winner', () => {
    const winner = mockGame.host;

    const res = shallow(<WinnerModal winner={winner} />);
    const modal = res.find(Modal);
    expect(modal).not.toBeNull();
    expect(modal.prop('show')).toBe(true);
    const title = modal.find(Modal.Title);
    expect(title.text()).toContain(winner);
});
