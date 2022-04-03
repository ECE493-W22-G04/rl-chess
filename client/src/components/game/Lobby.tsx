import React, { FC } from 'react';
import { Player } from '../../types';
import AuthService from '../../services/auth';

type LobbyProps = {
    host: Player;
};

const Lobby: FC<LobbyProps> = ({ host }: LobbyProps) => {
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
            <div>Waiting for enough players to begin</div>
            <div className="invite">Invite URL: {window.location.href}</div>
        </div>
    );
};

export default Lobby;
