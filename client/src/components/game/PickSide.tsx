import React, { FC } from 'react';
import socket from '../../services/socket';
import AuthService from '../../services/auth';

const PickSide: FC = () => {
    const handlePickBlack = () => {
        socket.emit('pick_side', { color: 'black', user: AuthService.getCurrentUser() });
    };
    const handlePickWhite = () => {
        socket.emit('pick_side', { color: 'white', user: AuthService.getCurrentUser() });
    };
    return (
        <div style={{ display: 'flex', flexDirection: 'row' }}>
            <button onClick={handlePickBlack}>Black</button>
            <button onClick={handlePickWhite}>White</button>
        </div>
    );
};

export default PickSide;
