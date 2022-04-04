import React from 'react';
import Modal from 'react-bootstrap/Modal';
import BoardTile from './BoardTile';

type PromotionModalProps = {
    isWhiteTurn: boolean;
    onTileClick: (promotion: number) => void;
};

const PromotionModal: React.FC<PromotionModalProps> = ({ isWhiteTurn, onTileClick }: PromotionModalProps) => {
    const handleClose = () => {
        // Default promote to queen
        if (isWhiteTurn) {
            onTileClick(6);
        } else {
            onTileClick(-6);
        }
    };

    const selectTile = (piece: number) => {
        onTileClick(piece);
    };

    const pieceOptions = [2, 3, 4, 5];

    return (
        <Modal show={true} onHide={handleClose} centered>
            <Modal.Header closeButton>
                <Modal.Title>Pawn Promotion</Modal.Title>
            </Modal.Header>
            <Modal.Body style={{ display: 'flex', flexFlow: 'row', gap: '1em' }}>
                {pieceOptions.map((piece) => {
                    // Use position as a unique key for the boardtile
                    const coloredPiece: number = isWhiteTurn ? piece : -piece;
                    return <BoardTile key={piece} onTileClick={() => selectTile(piece)} piece={coloredPiece} tileRow={0} tileCol={0} isSelected={false} />;
                })}
            </Modal.Body>
        </Modal>
    );
};

export default PromotionModal;
