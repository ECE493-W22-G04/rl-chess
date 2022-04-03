import React, { FC } from 'react';
import socket from '../../services/socket';
import AuthService from '../../services/auth';
import Button from 'react-bootstrap/Button';

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
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1em', alignItems: 'center' }}>
            <h3>Select Your Color </h3>
            <Button variant="dark" onClick={handlePickBlack}>
                Black
            </Button>
            <Button variant="light" onClick={handlePickWhite}>
                White
            </Button>
        </div>
    );
};

export default PickSide;
