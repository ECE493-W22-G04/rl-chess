import axios from 'axios';
const API_URL = 'http://localhost:5555/api/auth/';

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
        if (tokenStr) return tokenStr;
        return null;
    }
}

export default new AuthService();
