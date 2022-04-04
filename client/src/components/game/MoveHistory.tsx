import React from 'react';
import Container from 'react-bootstrap/Container';
import Table from 'react-bootstrap/Table';
import { SerializedMove, Move, Square } from '../../types';

type MoveHistoryProps = {
    gameMoves: SerializedMove[];
};

const MoveHistory: React.FC<MoveHistoryProps> = ({ gameMoves }: MoveHistoryProps) => {
    const moveArr: Move[] = gameMoves.map((move) => ({
        from_square: {
            x: move[0][0],
            y: move[0][1],
        },
        to_square: {
            x: move[1][0],
            y: move[1][1],
        },
        promotion: move[2],
    }));

    const moveNotation = (square: Square) => {
        switch (square.x) {
            case 0:
                return `a${square.y + 1}`;
            case 1:
                return `b${square.y + 1}`;
            case 2:
                return `c${square.y + 1}`;
            case 3:
                return `d${square.y + 1}`;
            case 4:
                return `e${square.y + 1}`;
            case 5:
                return `f${square.y + 1}`;
            case 6:
                return `g${square.y + 1}`;
            case 7:
                return `h${square.y + 1}`;
            default:
                return `a${square.y + 1}`;
        }
    };

    const promotionString = (promotion: number) => {
        switch (promotion) {
            case 2:
                return 'Bishop';
            case 3:
                return 'Knight';
            case 4:
                return 'Rook';
            case 5:
                return 'Queen';
            default:
                return 'None';
        }
    };

    return (
        <Container fluid="md">
            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>From</th>
                        <th>To</th>
                        <th>Promotion</th>
                    </tr>
                </thead>
                <tbody>
                    {moveArr.map((move, i) => (
                        <tr key={i}>
                            <td>{moveNotation(move.from_square)}</td>
                            <td>{moveNotation(move.to_square)}</td>
                            <td>{promotionString(move.promotion)}</td>
                        </tr>
                    ))}
                </tbody>
            </Table>
        </Container>
    );
};

export default MoveHistory;
