import React, { useEffect, useRef, useState } from 'react';
import { io } from 'socket.io-client';

export const Socket: React.FC = () => {
    const buttonRef = useRef<HTMLButtonElement>(null);
    const [isConnected, setIsConnected] = useState<boolean>(false);

    useEffect(() => {
        const socket = io('http://localhost:5555');
        socket.on('connect', () => {
            setIsConnected(true);
        });
        socket.on('disconnect', () => {
            setIsConnected(false);
        });

        if (!buttonRef.current) {
            return;
        }

        buttonRef.current.onclick = () => {
            socket.emit('click', {
                data: 'click',
            });
        };
    }, []);

    return (
        <div>
            <p>Server status: {isConnected ? 'True' : 'False'}</p>
            <button ref={buttonRef}>Send click</button>
        </div>
    );
};