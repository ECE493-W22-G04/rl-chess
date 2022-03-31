import React, { FC, useState, useEffect } from 'react';
import { Player } from '../../types';
import AuthService from '../../services/auth';
import PickSide from './PickSide';
import socket from '../../services/socket';

type LobbyProps = {
    gameId: string;
    host: Player;
};

const Lobby: FC<LobbyProps> = ({ gameId, host }: LobbyProps) => {
    const [roomFull, setRoomFull] = useState<boolean>(false);

    useEffect(() => {
        socket.on('room_full', () => {
            setRoomFull(true);
        });
    }, []);

    if (AuthService.getCurrentUser() !== host) {
        return (
            <div>
                <h1>Lobby</h1>
                Waiting for host
            </div>
        );
    }

    return (
        <div>
            <h1>Lobby</h1>
            {!roomFull && <div>Waiting for enough players to begin</div>}
            {AuthService.getCurrentUser() === host && roomFull && <PickSide gameId={gameId} />}
            <div className="invite">Invite URL: {window.location.href}</div>
        </div>
    );
};

export default Lobby;
