import React, { FC } from 'react';
import { Board as BoardType } from '../../types';

type BoardProps = {
    board: BoardType;
};

const Board: FC<BoardProps> = ({ board }: BoardProps) => {
    return <div>Board</div>;
};

export default Board;
