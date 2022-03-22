import React, { FC } from 'react';
import { ReactComponent as BishopSvg } from './pieces/bishop.svg';
import { ReactComponent as KingSvg } from './pieces/king.svg';
import { ReactComponent as KnightSvg } from './pieces/knight.svg';
import { ReactComponent as PawnSvg } from './pieces/pawn.svg';
import { ReactComponent as QueenSvg } from './pieces/queen.svg';
import { ReactComponent as RookSvg } from './pieces/rook.svg';
import { ReactComponent as EmptySvg } from './pieces/empty.svg';

type BoardTileProps = {
    piece: number;
    tileRow: number;
    tileCol: number;
};

const BoardTile: FC<BoardTileProps> = ({ piece, tileRow, tileCol }: BoardTileProps) => {
    const getTileColor = () => {
        const evenRow: boolean = tileRow % 2 == 0;
        const evenCol: boolean = tileCol % 2 == 0;
        if (evenRow === evenCol) {
            return '#f7e29c'; // light color
        } else {
            return '#8a7a45'; // dark color
        }
    };

    const tileStyle = {
        display: 'grid',
        placeItems: 'center',
        height: '4em',
        width: '4em',
        borderStyle: 'solid',
        borderWidth: '1px',
        backgroundColor: getTileColor(),
    };

    const pieceToSvg = (p: number) => {
        let pieceStyle = {};
        if (p < 0) {
            // Set piece color black/white
            pieceStyle = { filter: 'invert(100%)' };
        }

        if (Math.abs(p) == 1) {
            return <PawnSvg style={pieceStyle} />;
        } else if (Math.abs(p) == 2) {
            return <BishopSvg style={pieceStyle} />;
        } else if (Math.abs(p) == 3) {
            return <KnightSvg style={pieceStyle} />;
        } else if (Math.abs(p) == 4) {
            return <RookSvg style={pieceStyle} />;
        } else if (Math.abs(p) == 5) {
            return <QueenSvg style={pieceStyle} />;
        } else if (Math.abs(p) == 6) {
            return <KingSvg style={pieceStyle} />;
        }
        return <EmptySvg />;
    };

    return <div style={tileStyle}>{pieceToSvg(piece)}</div>;
};

export default BoardTile;
