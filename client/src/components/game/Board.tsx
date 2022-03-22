import React, { FC } from 'react';
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
    return (
        <div>
            {test_board.state.reverse().map((row, rowIndex) => (
                <div key={rowIndex.toString()} style={{ display: 'flex', flexDirection: 'row' }}>
                    {row.map((piece, colIndex) => {
                        // Use position as a unique key for the boardtile
                        const position = rowIndex.toString() + colIndex.toString();
                        return <BoardTile key={position} piece={piece} tileRow={rowIndex} tileCol={colIndex} />;
                    })}
                </div>
            ))}
        </div>
    );
};

export default Board;
