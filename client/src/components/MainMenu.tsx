import React, { FC } from 'react';
import { useNavigate } from 'react-router-dom';

import { createGame } from '../services/game';
import Button from 'react-bootstrap/Button';

const MainMenu: FC = () => {
    const navigate = useNavigate();
    const handlePlayAgainstComputer = async () => {
        const game = await createGame(false);
        navigate(`/game/${game.id}`);
    };

    const handlePlayAgainstPlayer = async () => {
        const game = await createGame(true);
        navigate(`/game/${game.id}`);
    };

    return (
        <div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1em', alignItems: 'center' }}>
                <h1>Main menu</h1>
                <Button id={'pvc'} onClick={handlePlayAgainstComputer}>
                    Play against computer
                </Button>
                <Button id={'pvp'} onClick={handlePlayAgainstPlayer}>
                    Play against player
                </Button>
            </div>
        </div>
    );
};

export default MainMenu;
