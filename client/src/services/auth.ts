import axios from 'axios';
import jwtDecode from 'jwt-decode';
import config from '../config';
import { Jwt } from '../types';

const API_URL = `${config.SERVER_ENDPOINT}/api/auth/`;

class AuthService {
    login(email: string, password: string) {
        return axios
            .post(API_URL + 'signin', {
                email,
                password,
            })
            .then((response) => {
                if (response.data.access_token) {
                    localStorage.setItem('token', response.data.access_token);
                }
                return response.data;
            });
    }
    logout() {
        localStorage.removeItem('token');
    }
    register(email: string, password: string) {
        return axios.post(API_URL + 'signup', {
            email,
            password,
        });
    }
    getCurrentUser() {
        const tokenStr = localStorage.getItem('token');
        if (tokenStr == null) {
            return null;
        }
        const jwt = jwtDecode<Jwt>(tokenStr);
        return jwt.sub;
    }
}

export default new AuthService();
