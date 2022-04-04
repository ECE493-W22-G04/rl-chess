import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import logo from '../logo.svg';
import AuthService from '../services/auth';

const Header: React.FC = () => {
    const [currentUser, setCurrentUser] = useState<string>('');
    const logout = () => {
        AuthService.logout();
        setCurrentUser('');
    };

    useEffect(() => {
        const user = AuthService.getCurrentUser();
        if (user) {
            setCurrentUser(user);
        }
    }, []);

    return (
        <nav className="navbar navbar-expand navbar-dark bg-dark">
            <Link to={'/'} className="navbar-brand">
                <img src={logo} className="App-logo" alt="logo" />
                RL Chess
            </Link>
            {currentUser ? (
                <div className="navbar-nav ml-auto">
                    <li className="nav-item">
                        <Link to={'/leaderboard'} className="nav-link">
                            Leaderboard
                        </Link>
                    </li>
                    <li className="nav-item">
                        <a href="/login" className="nav-link" onClick={logout}>
                            Logout
                        </a>
                    </li>
                </div>
            ) : (
                <div className="navbar-nav ml-auto">
                    <li className="nav-item">
                        <Link to={'/login'} className="nav-link">
                            Login
                        </Link>
                    </li>
                    <li className="nav-item">
                        <Link to={'/register'} className="nav-link">
                            Sign Up
                        </Link>
                    </li>
                </div>
            )}
        </nav>
    );
};

export default Header;
