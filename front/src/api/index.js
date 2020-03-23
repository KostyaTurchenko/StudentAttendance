import axios from 'axios'

const API_URL = 'http://127.0.0.1:5000';

export function authenticate (userData) {
    return axios.post(`${API_URL}/login`, userData)
}

export function getStudents (jwt) {
    console.log(jwt);
    return axios.get(`${API_URL}/students`, {}, { headers: { Authorization: `Bearer: ${jwt}` } });
}
