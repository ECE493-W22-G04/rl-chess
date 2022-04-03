import axios from 'axios';
import config from '../config';
import authHeader from './auth-header';

const API_URL = `${config.SERVER_ENDPOINT}/api/games/`;

export async function createGame(isPvP: boolean) {
    const payload = {
        isPvP,
    };
    try {
        const resp = await axios.post(API_URL, payload, {
            headers: authHeader(),
        });
        return JSON.parse(resp.data);
    } catch (err) {
        console.error(err);
        // Many errors are caused by bad token so clear it and refresh
        localStorage.clear();
        window.location.reload();
        return null;
    }
}

export async function getGameDetails(gameId: string) {
    try {
        const resp = await axios.get(`${API_URL}${gameId}`, {
            headers: authHeader(),
        });
        return JSON.parse(resp.data);
    } catch (err) {
        console.error(err);
        // Many errors are caused by bad token so clear it and refresh
        localStorage.clear();
        window.location.reload();
        return null;
    }
}
