import React, { FC, useEffect, useState } from 'react';
import { Navigate, useParams } from 'react-router-dom';
import Board from './Board';
import Lobby from './Lobby';
import { getGameDetails } from '../../services/game';
import socket from '../../services/socket';
import { Game } from '../../types';
import AuthService from '../../services/auth';
import PickSide from './PickSide';

const Room: FC = () => {
    const { gameId } = useParams();
    const [game, setGame] = useState<Game | null>(null);
    const [isGameReady, setIsGameReady] = useState<boolean>(false);
    const [hasGameStarted, setHasGameStarted] = useState<boolean>(false);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        if (gameId == null) {
            return;
        }
        (async () => {
            const gameDetails = await getGameDetails(gameId);
            setGame(gameDetails);
            setIsLoading(false);
        })();
    }, []);

    useEffect(() => {
        socket.on('room_full', () => {
            setIsGameReady(true);
        });

        socket.on('update', (data) => {
            const new_game: Game = JSON.parse(data);
            setGame(new_game);
        });

        socket.on('message', (data) => {
            console.log(data);
        });
    }, []);

    useEffect(() => {
        socket.emit('join', { user: AuthService.getCurrentUser(), gameId: gameId });
    }, [game]);

    if (isLoading) {
        return <div>Loading...</div>;
    }

    if (game == null) {
        return <Navigate to="/" />;
    }

    if (!game.has_started) {
        if (!isGameReady) {
            return <Lobby host={game.host} />;
        }
        if (game.host == AuthService.getCurrentUser()) {
            return <PickSide gameId={game.id} />;
        }
    }

    return <Board game={game} />;
};

export default Room;
