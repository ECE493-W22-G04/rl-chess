import React, { FC, useEffect, useState } from 'react';
import { Navigate, useParams } from 'react-router-dom';
import Board from './Board';
import Lobby from './Lobby';
import { getGameDetails } from '../../services/game';
import socket from '../../services/socket';
import { Game } from '../../types';

const Room: FC = () => {
    const { gameId } = useParams();
    const [game, setGame] = useState<Game | null>(null);
    const [hasGameStarted, setHasGameStarted] = useState<boolean>(false);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        socket.on('start_game', () => {
            setHasGameStarted(true);
        });
        socket.on('update', (game: Game) => {
            setGame(game);
        });
    }, []);

    useEffect(() => {
        if (gameId == null) {
            return;
        }
        (async () => {
            setGame(await getGameDetails(gameId));
            setIsLoading(false);
        })();
    }, []);

    if (isLoading) {
        return <div>Loading...</div>;
    }

    if (game === null) {
        return <Navigate to="/" />;
    }

    if (!hasGameStarted) {
        return <Lobby gameId={game.id} host={game.host} />;
    }

    return <Board board={game.board} />;
};

export default Room;