import React, { useState } from 'react';
import './App.css';

function App() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const token = sessionStorage.getItem('token');
    console.log('This is your token', token);

    const handleClick = () => {
        const opts = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                password: password,
            }),
        };

        fetch('http://localhost:5555/token', opts)
            .then((resp) => {
                if (resp.status === 200) return resp.json();
                else alert('There has been some error');
            })
            .then((data) => {
                sessionStorage.setItem('token', data.access_token);
            })
            .catch((error) => {
                console.error('There was an error:' + error);
            });
    };

    return (
        <div className="App">
            <header className="App-header">
                <h1>Login</h1>
                {token && token != '' && token != undefined ? (
                    'You are logged in with ' + token
                ) : (
                    <div>
                        <input
                            type="text"
                            placeholder="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                        <input
                            type="password"
                            placeholder="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                        <button onClick={handleClick}>Login</button>
                    </div>
                )}
            </header>
        </div>
    );
}

export default App;
