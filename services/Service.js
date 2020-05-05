import axios from 'axios'

const apiClient = axios.create({
  // baseURL: `//localhost:3000`,
  baseURL: `https://api-tt-2019-b052.herokuapp.com`,
  withCredentials: false,
  progress: true,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json'
  }
})

export default {
  async register(signupInfo) {
    const ip = await apiClient.post('/user', signupInfo)
    return ip
  },
  async login(credentials) {
    const ip = await apiClient.post('/login', credentials)
    return ip
  },
  setToken(userData) {
    axios.defaults.headers.common.Authorization = `Bearer ${userData.token}`
  }
}
