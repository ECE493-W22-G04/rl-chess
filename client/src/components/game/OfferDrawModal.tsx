import React, { useState, useEffect } from 'react';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import socket from '../../services/socket';
import AuthService from '../../services/auth';
import { OfferDrawMessage } from '../../types';

type OfferDrawModalProps = {
    gameId: string | null;
};

const OfferDrawModal: React.FC<OfferDrawModalProps> = ({ gameId }: OfferDrawModalProps) => {
    const [isModalShown, setIsModalShown] = useState<boolean>(false);
    const handleClose = () => {
        setIsModalShown(false);
    };

    useEffect(() => {
        socket.on('offer_draw', (data) => {
            const msg: OfferDrawMessage = JSON.parse(data);
            if (AuthService.getCurrentUser() == msg.offer_draw_to) {
                setIsModalShown(true);
            }
        });
    }, []);

    const acceptDraw = () => {
        socket.emit('accept_draw', { gameId: gameId });
        handleClose();
    };

    return (
        <Modal show={isModalShown} onHide={handleClose} centered>
            <Modal.Header closeButton>
                <Modal.Title>Draw Offer</Modal.Title>
            </Modal.Header>
            <Modal.Body>Your opponent has offered you a draw, will you accept?</Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={handleClose}>
                    Decline
                </Button>
                <Button variant="primary" onClick={acceptDraw}>
                    Accept
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

export default OfferDrawModal;
