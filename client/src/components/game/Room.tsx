import React, { FC, useEffect, useState } from 'react';
import { Navigate, useParams } from 'react-router-dom';
import Board from './Board';
import Lobby from './Lobby';
import { getGameDetails } from '../../services/game';
import socket from '../../services/socket';
import { Game, GameOverMessage, Player } from '../../types';
import AuthService from '../../services/auth';
import PickSide from './PickSide';
import WinnerModal from './WinnerModal';
import OfferDrawModal from './OfferDrawModal';
import PlayersInRoom from './PlayersInRoom';

const Room: FC = () => {
    const { gameId } = useParams();
    const [game, setGame] = useState<Game | null>(null);
    const [isGameReady, setIsGameReady] = useState<boolean>(false);
    const [isLoading, setIsLoading] = useState(true);
    const [winner, setWinner] = useState<string | null>(null);
    const [players, setPlayers] = useState<Player[]>([]);

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

        socket.on('players_in_room', (players_in_room) => {
            setPlayers(players_in_room);
        });

        socket.on('message', (data) => {
            console.log(data);
        });

        socket.on('game_over', (data) => {
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
        if (isGameReady && game.host == AuthService.getCurrentUser()) {
            return (
                <div>
                    <PlayersInRoom players={players}></PlayersInRoom>
                    <PickSide gameId={game.id} />
                </div>
            );
        }
        return (
            <div>
                <PlayersInRoom players={players}></PlayersInRoom>
                <Lobby host={game.host} />
            </div>
        );
    }

    return (
        <>
            <WinnerModal winner={winner} />
            <OfferDrawModal gameId={game.id} />
            <PlayersInRoom players={players}></PlayersInRoom>
            <br />
            <Board game={game} />
        </>
    );
};

export default Room;
