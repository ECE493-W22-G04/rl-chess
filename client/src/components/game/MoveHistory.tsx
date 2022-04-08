import React from 'react';
import Card from 'react-bootstrap/Card';
import Table from 'react-bootstrap/Table';
import { SerializedMove, Move, Square } from '../../types';

// This File is used to satisfy the following functional requirements:
// FR21 - Board.History

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
        const charX = String.fromCharCode(97 + square.x);
        const yVal = 8 - square.y;
        return `${charX}${yVal}`;
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
                return '-';
        }
    };

    return (
        <Card style={{ display: 'flex', height: '32em' }}>
            <Card.Header>Move History</Card.Header>
            <Card.Body style={{ overflowY: 'scroll' }}>
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
            </Card.Body>
        </Card>
    );
};

export default MoveHistory;
