import React, { useEffect, useState } from 'react';
import { io } from 'socket.io-client';

export const Socket: React.FC = () => {
    const [isConnected, setIsConnected] = useState<boolean>(false);

    useEffect(() => {
        const socket = io('http://localhost:5555');
        socket.on('connect', () => {
            setIsConnected(true);
        });
        socket.on('disconnect', () => {
            setIsConnected(false);
        });
    }, []);

    return (
        <div>
            <p>Server status: {isConnected ? 'True' : 'False'}</p>
        </div>
    );
};
