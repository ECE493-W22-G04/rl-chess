import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import Login from './components/login';
import Register from './components/register';
import Header from './components/Header';
import RequireAuth from './services/RequireAuth';
import MainMenu from './components/MainMenu';
import Room from './components/game/Room';
import Leaderboard from './components/Leaderboard';

const App: React.FunctionComponent = () => {
    return (
        <BrowserRouter>
            <Header />
            <div className="container-fluid mt-3">
                <Routes>
                    <Route
                        path="/"
                        element={
                            <RequireAuth>
                                <MainMenu />
                            </RequireAuth>
                        }
                    />
                    <Route
                        path="/game/:gameId"
                        element={
                            <RequireAuth>
                                <Room />
                            </RequireAuth>
                        }
                    />
                    <Route
                        path="/leaderboard"
                        element={
                            <RequireAuth>
                                <Leaderboard />
                            </RequireAuth>
                        }
                    />
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                </Routes>
            </div>
        </BrowserRouter>
    );
};

export default App;
