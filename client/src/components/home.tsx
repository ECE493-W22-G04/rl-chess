import React, { useState, useEffect } from 'react';
import UserService from '../services/user';

const Home: React.FunctionComponent = () => {
    const [content, setContent] = useState<string | undefined>(undefined);
    useEffect(() => {
        const tokenStr = localStorage.getItem('token');
        if (!tokenStr) {
            UserService.getPublicContent().then(
                (response) => {
                    setContent(response.data.message);
                },
                (error) => {
                    setContent(
                        (error.response && error.response.data) ||
                            error.message ||
                            error.toString()
                    );
                }
            );
        } else {
            UserService.getUserBoard().then(
                (response) => {
                    setContent(response.data.message);
                },
                (error) => {
                    setContent(
                        (error.response && error.response.data) ||
                            error.message ||
                            error.toString()
                    );
                }
            );
        }
    }, []);
    return (
        <div className="container">
            <header className="jumbotron">
                <h3>{content}</h3>
            </header>
        </div>
    );
};

export default Home;
