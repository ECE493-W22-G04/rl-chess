import axios from 'axios';
import config from '../config';
import authHeader from './auth-header';

const API_URL = `${config.SERVER_ENDPOINT}/api/leaderboard/`;

export async function getLeaderboard() {
    try {
        const resp = await axios.get(API_URL, {
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