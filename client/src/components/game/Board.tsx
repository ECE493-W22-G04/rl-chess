import React, { FC, useEffect, useState } from 'react';
import { Game } from '../../types';
import BoardTile from './BoardTile';
import socket from '../../services/socket';

type BoardProps = {
    game: Game;
};

type Tile = [number, number];

const Board: FC<BoardProps> = ({ game }: BoardProps) => {
    const [tile1, setTile1] = useState<Tile | null>(null);
    const [tile2, setTile2] = useState<Tile | null>(null);

    useEffect(() => {
        if (tile1 && tile2) {
            console.log(`Selected Move from ${tile1} to ${tile2}`);
            socket.emit('make_move', { gameId: game.id, moveStr: `${tile1}->${tile2}` });
            setTile1(null);
            setTile2(null);
        }
    }, [tile2]);

    const selectTile = (tile: Tile) => {
        console.log(`Selected Tile: ${tile}`);
        if (!tile1) {
            setTile1(tile);
        } else if (!tile2) {
            setTile2(tile);
        } else {
            console.log('HOW DID THIS HAPPEN!');
        }
    };

    return (
        <div>
            {game.board.state.reverse().map((row, rowIndex) => (
                <div key={`${rowIndex}`} style={{ display: 'flex', flexDirection: 'row' }}>
                    {row.map((piece, colIndex) => {
                        // Use position as a unique key for the boardtile
                        const position: Tile = [colIndex, rowIndex];
                        return <BoardTile key={`${position}`} onTileClick={() => selectTile(position)} piece={piece} tileRow={rowIndex} tileCol={colIndex} isSelected={`${position}` === `${tile1}`} />;
                    })}
                </div>
            ))}
        </div>
    );
};

export default Board;
