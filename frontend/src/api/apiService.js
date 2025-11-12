import axios from 'axios';

const apiClient = axios.create({
    baseURL: process.env.REACT_APP_API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const createAlerta = (alertaData) => {
    return apiClient.post('/alertas/', alertaData);
};
