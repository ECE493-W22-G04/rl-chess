import React, { useEffect, useState } from 'react';
import Container from 'react-bootstrap/Container';
import Table from 'react-bootstrap/Table';
import { getLeaderboard } from '../services/leaderboard';
import { Leaderboard as LeaderboardType } from '../types';

// This File is used to satisfy the following functional requirements:
// FR30 - Display.Leaderboard

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
        <Container fluid="md">
            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Email</th>
                        <th>Number of computer matches won</th>
                        <th>Number of computer matches played</th>
                        <th>Win rate against computer</th>
                    </tr>
                </thead>
                <tbody>
                    {entries?.map((entry, i) => (
                        <tr key={i}>
                            <td>{i + 1}</td>
                            <td>{entry.email}</td>
                            <td>{entry.numGamesWon}</td>
                            <td>{entry.numGamesPlayed}</td>
                            <td>{(entry.winRate * 100).toFixed(1)}%</td>
                        </tr>
                    ))}
                </tbody>
            </Table>
        </Container>
    );
};

export default Leaderboard;
