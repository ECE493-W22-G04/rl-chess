import React, { FC, useEffect, useState } from 'react';
import { Board as BoardType } from '../../types';
import BoardTile from './BoardTile';

type BoardProps = {
    board: BoardType;
};

// Temp board used for testing
const test_board: BoardType = {
    state: [
        [-4, -3, -2, -5, -6, -2, -3, -4],
        [-1, -1, -1, -1, -1, -1, -1, -1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [4, 3, 2, 5, 6, 2, 3, 4],
    ],
    isWhiteTurn: true,
};

const Board: FC<BoardProps> = ({ board }: BoardProps) => {
    const [tile1, setTile1] = useState<string | null>(null);
    const [tile2, setTile2] = useState<string | null>(null);

    useEffect(() => {
        document;
    }, [tile1]);

    useEffect(() => {
        if (tile1 && tile2) {
            console.log(`Selected Move ${tile1}${tile2}`);
            setTile1(null);
            setTile2(null);
        }
    }, [tile2]);

    const selectTile = (tile: string) => {
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
            {test_board.state.reverse().map((row, rowIndex) => (
                <div key={rowIndex.toString()} style={{ display: 'flex', flexDirection: 'row' }}>
                    {row.map((piece, colIndex) => {
                        // Use position as a unique key for the boardtile
                        const position = colIndex.toString() + rowIndex.toString();
                        return <BoardTile key={position} onTileClick={() => selectTile(position)} piece={piece} tileRow={rowIndex} tileCol={colIndex} isSelected={position == tile1} />;
                    })}
                </div>
            ))}
        </div>
    );
};

export default Board;
