import React, { FC } from 'react';
import { Player } from '../../types';
import Card from 'react-bootstrap/Card';

type PlayersInRoomProps = {
    players: Player[];
};

const PlayersInRoom: FC<PlayersInRoomProps> = ({ players }: PlayersInRoomProps) => {
    const formattedPlayers = () => {
        if (players.length == 1) {
            return <Card.Header>{'Host: ' + players[0]}</Card.Header>;
        } else if (players.length == 2) {
            return (
                <Card.Header>
                    <div>{'Host: ' + players[0]}</div> <div>{'Guest: ' + players[1]}</div>
                </Card.Header>
            );
        } else {
            return <></>;
        }
    };
    return <Card>{formattedPlayers()}</Card>;
};

export default PlayersInRoom;
