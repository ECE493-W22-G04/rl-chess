import React, { FC, useEffect, useState } from 'react';
import { Game } from '../../types';
import BoardTile from './BoardTile';
import socket from '../../services/socket';
import AuthService from '../../services/auth';

type BoardProps = {
    game: Game;
};

type Tile = [number, number];

const Board: FC<BoardProps> = ({ game }: BoardProps) => {
    const [tile1, setTile1] = useState<Tile | null>(null);
    const [tile2, setTile2] = useState<Tile | null>(null);
    const [displayMessage, setDisplayMessage] = useState<string>('');
    const [playerColor, setPlayerColor] = useState<string>('');

    useEffect(() => {
        socket.on('message', (data) => {
            setDisplayMessage(data);
        });

        // Set player color
        if (AuthService.getCurrentUser() == game.white_player) {
            setPlayerColor('white');
        } else {
            setPlayerColor('black');
        }
    }, []);

    useEffect(() => {
        if (tile1 && tile2) {
            socket.emit('make_move', { gameId: game.id, moveStr: `${tile1}->${tile2}` });
            setTile1(null);
            setTile2(null);
        }
    }, [tile2]);

    const currentTurn = () => {
        return game.board.is_white_turn ? 'white' : 'black';
    };

    const selectTile = (tile: Tile) => {
        // reset message on click
        setDisplayMessage('');

        if (currentTurn() == playerColor) {
            if (!tile1) {
                setTile1(tile);
            } else if (!tile2) {
                setTile2(tile);
            } else {
                console.log('HOW DID THIS HAPPEN!');
            }
        } else {
            setDisplayMessage('It is not your turn.');
        }
    };

    const offerDraw = () => {
        socket.emit('offer_draw', { gameId: game.id, currentPlayer: AuthService.getCurrentUser() });
    };

    const concede = () => {
        socket.emit('concede', { gameId: game.id, currentPlayer: AuthService.getCurrentUser() });
    };

    return (
        <div style={{ display: 'flex', flexFlow: 'row wrap', gap: '2em', justifyContent: 'center' }}>
            <div className="board">
                {game.board.state.map((row, rowIndex) => (
                    <div key={`${rowIndex}`} style={{ display: 'flex', flexDirection: 'row' }}>
                        {row.map((piece, colIndex) => {
                            // Use position as a unique key for the boardtile
                            const position: Tile = [colIndex, rowIndex];
                            return (
                                <BoardTile key={`${position}`} onTileClick={() => selectTile(position)} piece={piece} tileRow={rowIndex} tileCol={colIndex} isSelected={`${position}` === `${tile1}`} />
                            );
                        })}
                    </div>
                ))}
            </div>
            <div style={{ borderStyle: 'solid', display: 'flex', flexFlow: 'column wrap', justifyContent: 'space-evenly', alignItems: 'center', padding: '2em' }}>
                <div className="player-color">
                    <h2>You are playing {playerColor}</h2>
                </div>
                <div className="current-turn">
                    <h2>Current turn {currentTurn()}</h2>
                </div>
                <div className="offer-draw">{game.black_player != null && game.white_player != null && <button onClick={offerDraw}>Offer Draw</button>}</div>
                <div className="concede">
                    <button onClick={concede}>Concede</button>
                </div>
                <div className="display-message">{displayMessage && <div className="alert alert-warning">{displayMessage}</div>}</div>
            </div>
        </div>
    );
};

export default Board;
