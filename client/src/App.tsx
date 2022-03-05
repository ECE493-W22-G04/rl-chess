import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import AuthService from './services/auth';
import Login from './components/login';
import Register from './components/register';
import Home from './components/home';

const App: React.FunctionComponent = () => {
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
        <BrowserRouter>
            <nav className="navbar navbar-expand navbar-dark bg-dark">
                <Link to={'/'} className="navbar-brand">
                    RL Chess
                </Link>
                {currentUser ? (
                    <div className="navbar-nav ml-auto">
                        <li className="nav-item">
                            <a
                                href="/login"
                                className="nav-link"
                                onClick={logout}
                            >
                                LogOut
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
            <div className="container mt-3">
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                </Routes>
            </div>
        </BrowserRouter>
    );
};

export default App;
