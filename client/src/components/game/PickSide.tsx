import React, { FC } from 'react';
import socket from '../../services/socket';
import AuthService from '../../services/auth';

type PickSideProps = {
    gameId: string;
};

const PickSide: FC<PickSideProps> = ({ gameId }: PickSideProps) => {
    const handlePickBlack = () => {
        socket.emit('pick_side', { gameId: gameId, color: 'black', user: AuthService.getCurrentUser() });
    };
    const handlePickWhite = () => {
        socket.emit('pick_side', { gameId: gameId, color: 'white', user: AuthService.getCurrentUser() });
    };
    return (
        <div style={{ display: 'flex', flexDirection: 'row' }}>
            <h3>Select Your Color </h3>
            <button onClick={handlePickBlack}>Black</button>
            <button onClick={handlePickWhite}>White</button>
        </div>
    );
};

export default PickSide;
