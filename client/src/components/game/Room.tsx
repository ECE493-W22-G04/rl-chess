import React, { FC, useEffect, useState } from 'react';
import { Navigate, useParams } from 'react-router-dom';
import Board from './Board';
import Lobby from './Lobby';
import { getGameDetails } from '../../services/game';
import socket from '../../services/socket';
import { Game, GameOverMessage } from '../../types';
import AuthService from '../../services/auth';
import PickSide from './PickSide';
import WinnerModal from './WinnerModal';

const Room: FC = () => {
    const { gameId } = useParams();
    const [game, setGame] = useState<Game | null>(null);
    const [isGameReady, setIsGameReady] = useState<boolean>(false);
    const [isLoading, setIsLoading] = useState(true);
    const [winner, setWinner] = useState<string | null>(null);

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

        socket.on('game-over', (data) => {
            const msg: GameOverMessage = JSON.parse(data);
            setWinner(msg.winner);
        });
    }, []);

    useEffect(() => {
        socket.emit('join', { user: AuthService.getCurrentUser(), gameId: gameId });
    }, [game]);

    if (isLoading) {
        return <div>Loading...</div>;
    }

    if (game == null) {
        console.error(`Could not find game with id ${gameId}`);
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

    return (
        <>
            <WinnerModal winner={winner} />
            <Board game={game} />
        </>
    );
};

export default Room;
