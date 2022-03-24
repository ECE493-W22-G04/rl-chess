import React, { FC } from 'react';
import { useNavigate } from 'react-router-dom';

import { createGame } from '../services/game';

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
            <h1>Main menu</h1>
            <div style={{ display: 'flex', flexDirection: 'row' }}>
                <button id={'pvc'} onClick={handlePlayAgainstComputer}>
                    Play against computer
                </button>
                <button id={'pvp'} onClick={handlePlayAgainstPlayer}>
                    Play against player
                </button>
            </div>
        </div>
    );
};

export default MainMenu;
