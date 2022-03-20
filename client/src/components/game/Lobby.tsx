import React, { FC } from 'react';
import socket from '../../services/socket';
import { Player } from '../../types';
import AuthService from '../../services/auth';
import PickSide from './PickSide';

type LobbyProps = {
    gameId: number;
    host: Player;
};

const Lobby: FC<LobbyProps> = ({ gameId, host }: LobbyProps) => {
    const broadcastGameStarted = () => {
        socket.emit('start_game', {
            gameId,
        });
    };

    return (
        <div>
            <h1>Lobby</h1>
            <button
                onClick={() => {
                    broadcastGameStarted();
                }}
            >
                Start game
            </button>
            {AuthService.getCurrentUser() === host && <PickSide />}
        </div>
    );
};

export default Lobby;
