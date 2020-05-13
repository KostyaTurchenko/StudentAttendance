import axios from 'axios'

const API_URL = 'http://127.0.0.1:5000';

const token = localStorage.getItem('token')
if (token) {
  axios.defaults.headers.common['Authorization'] = `Bearer: ${token}`;
}

export function setToken (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer: ${token}`;
}

export function authenticate (userData) {
    return axios.post(`${API_URL}/login`, userData)
}

export function getGroups (course) {
    return axios.post(`${API_URL}/groups`, course)
}

export function getStudents (query) {
    return axios.post(`${API_URL}/students`, query);
}

export function addAbsenteeism (query) {
    return axios.post(`${API_URL}/absenteeism/add`, query);
}

/*export function getCourses () {
    return axios.get(`${API_URL}/courses`);
}*/

export function removeAbsenteeism (query) {
    return axios.post(`${API_URL}/absenteeism/remove`, query);
}
