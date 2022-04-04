import React, { FC, useEffect, useState } from 'react';
import { Game } from '../../types';
import BoardTile from './BoardTile';
import socket from '../../services/socket';
import AuthService from '../../services/auth';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import PromotionModal from './PromotionModal';

type BoardProps = {
    game: Game;
};

type Tile = [number, number];

const Board: FC<BoardProps> = ({ game }: BoardProps) => {
    const [tile1, setTile1] = useState<Tile | null>(null);
    const [tile2, setTile2] = useState<Tile | null>(null);
    const [displayMessage, setDisplayMessage] = useState<string>('');
    const [playerColor, setPlayerColor] = useState<string>('');
    const [isPromotion, setIsPromotion] = useState<boolean>(false);

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

    const makeMove = (promotion: number) => {
        if (tile1 != null && tile2 != null) {
            console.log('sending move');
            socket.emit('make_move', { gameId: game.id, moveStr: `${tile1}->${tile2}`, promotion: promotion });
            setTile1(null);
            setTile2(null);
        } else {
            console.log('unable to make move ' + tile1 + tile2 + promotion);
        }
    };

    useEffect(() => {
        checkForPromotion();
    }, [tile2]);

    const checkForPromotion = () => {
        if (tile1 != null && tile2 != null) {
            const tile1Piece = game.board.state[tile1[1]][tile1[0]];
            // Check piece is a pawn and check if tile2 is end of board
            console.log('Piece1 ' + Math.abs(tile1Piece));
            if (Math.abs(tile1Piece) == 1 && (tile2[1] == 0 || tile2[1] == 7)) {
                setIsPromotion(true);
            } else {
                // make move with no promotion
                makeMove(0);
            }
        }
    };

    const selectPromotion = (prom: number) => {
        setIsPromotion(false);
        makeMove(prom);
    };

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
            {isPromotion && <PromotionModal isWhiteTurn={game.board.is_white_turn} onTileClick={(promotion: number) => selectPromotion(promotion)} />}
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
            <Card style={{ display: 'flex', flexFlow: 'column wrap', justifyContent: 'space-evenly', alignItems: 'center', padding: '2em' }}>
                <div className="player-color">
                    <h2>You are playing {playerColor}</h2>
                </div>
                <div className="current-turn">
                    <h2>Current turn {currentTurn()}</h2>
                </div>
                <div className="offer-draw">{game.black_player != null && game.white_player != null && <Button onClick={offerDraw}>Offer Draw</Button>}</div>
                <div className="concede">
                    <Button onClick={concede}>Concede</Button>
                </div>
                <div className="display-message">{displayMessage && <div className="alert alert-warning">{displayMessage}</div>}</div>
            </Card>
        </div>
    );
};

export default Board;
