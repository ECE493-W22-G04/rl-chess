export default function authHeader() {
    let tokenStr = localStorage.getItem('token');
    if (!tokenStr) tokenStr = '';
    return { Authorization: tokenStr };
}
