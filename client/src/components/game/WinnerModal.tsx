import React, { useState } from 'react';
import Modal from 'react-bootstrap/Modal';

type WinnerModalProps = {
    winner: string | null;
};

const WinnerModal: React.FC<WinnerModalProps> = ({ winner }: WinnerModalProps) => {
    const [isModalShown, setIsModalShown] = useState<boolean>(true);
    if (winner == null) {
        return <></>;
    }
    const handleClose = () => {
        setIsModalShown(false);
    };
    return (
        <Modal show={isModalShown} onHide={handleClose} centered>
            <Modal.Header closeButton>
                <Modal.Title>{winner} is the winner!</Modal.Title>
            </Modal.Header>
        </Modal>
    );
};

export default WinnerModal;
