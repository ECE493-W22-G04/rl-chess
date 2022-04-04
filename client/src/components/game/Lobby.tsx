import React, { FC } from 'react';
import { Player } from '../../types';
import AuthService from '../../services/auth';
import Card from 'react-bootstrap/Card';

type LobbyProps = {
    host: Player;
};

const Lobby: FC<LobbyProps> = ({ host }: LobbyProps) => {
    if (AuthService.getCurrentUser() !== host) {
        return (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1em', alignItems: 'center' }}>
                <h1>Lobby</h1>
                Waiting for host
            </div>
        );
    }

    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1em', alignItems: 'center' }}>
            <h1>Lobby</h1>
            <div>Waiting for enough players to begin</div>
            <div>Invite URL: </div>
            <Card>
                <Card.Body>{window.location.href}</Card.Body>
            </Card>
        </div>
    );
};

export default Lobby;
