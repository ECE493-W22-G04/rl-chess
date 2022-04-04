import React, { useEffect, useState } from 'react';
import Table from 'react-bootstrap/Table';
import { getLeaderboard } from '../services/leaderboard';
import { Leaderboard as LeaderboardType } from '../types';

const Leaderboard: React.FC = () => {
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const [entries, setEntries] = useState<LeaderboardType | null>(null);

    useEffect(() => {
        (async () => {
            setEntries(await getLeaderboard());
            setIsLoading(false);
        })();
    }, []);

    if (isLoading) {
        return <p>Loading...</p>;
    }

    return (
        <Table striped bordered hover>
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>Email</th>
                    <th>Number of wins</th>
                </tr>
            </thead>
            <tbody>
                {entries?.map((entry, i) => (
                    <tr key={i}>
                        <td>i</td>
                        <td>{entry.email}</td>
                        <td>{entry.numWins}</td>
                    </tr>
                ))}
            </tbody>
        </Table>
    );
};

export default Leaderboard;
