import axios from 'axios';
import authHeader from './auth-header';
import config from '../config';

const API_URL = `${config.SERVER_ENDPOINT}/api/`;

class UserService {
    getPublicContent() {
        return axios.get(API_URL + 'home');
    }
    getUserBoard() {
        return axios.get(API_URL + 'user', { headers: authHeader() });
    }
}
export default new UserService();
