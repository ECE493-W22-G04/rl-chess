import React, { useEffect, useState } from 'react';
import socket from './services/socket';

export const Socket: React.FC = () => {
    const [isConnected, setIsConnected] = useState<boolean>(false);

    useEffect(() => {
        socket.on('connect', () => {
            setIsConnected(true);
        });
        socket.on('disconnect', () => {
            setIsConnected(false);
        });
    }, []);

    const handleClick = () => {
        socket.emit('click', {
            data: 'click',
        });
    };

    return (
        <div>
            <p>Server status: {isConnected ? 'True' : 'False'}</p>
            <button onClick={handleClick}>Send click</button>
        </div>
    );
};
