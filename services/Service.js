import axios from 'axios'

const apiClient = axios.create({
  baseURL: `//localhost:3000`,
  withCredentials: false,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json'
  }
})

export default {
  register(signupInfo) {
    return apiClient.post('/register', signupInfo)
  },
  login(credentials) {
    return apiClient.post('/login', credentials)
  },
  setToken(userData) {
    axios.defaults.headers.common.Authorization = `Bearer ${userData.token}`
  }
}
