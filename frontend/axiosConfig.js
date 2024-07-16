import axios from 'axios';

// Configura Axios para incluir cookies en las solicitudes
axios.defaults.withCredentials = true;

export default axios;