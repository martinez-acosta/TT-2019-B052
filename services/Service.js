import axios from 'axios'

const apiClient = axios.create({
  baseURL: `//localhost:5000`,
  // baseURL: `https://api-tt-2019-b052.herokuapp.com`,
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
  async saveDiagram(dataModel) {
    const token = axios.defaults.headers.common.Authorization
    return await apiClient.post(
      '/diagram',
      { diagram: dataModel },
      {
        headers: {
          Authorization: token
        }
      }
    )
  },
  async getLastDiagram() {
    const token = axios.defaults.headers.common.Authorization
    return await apiClient.get('/diagram', {
      headers: {
        Authorization: token
      }
    })
  },
  setToken(userData) {
    axios.defaults.headers.common.Authorization = `Bearer ${userData.token}`
  },
  async validateDiagram(diagram) {
    const token = axios.defaults.headers.common.Authorization
    return await apiClient.post(
      '/relational/validate',
      { diagram },
      {
        headers: {
          Authorization: token
        }
      }
    )
  },
  async convertToSQL(payload) {
    const token = axios.defaults.headers.common.Authorization
    return await apiClient.post('/relational', payload, {
      headers: {
        Authorization: token
      }
    })
  },
  async getNoSQLDiagram(payload) {
    const token = axios.defaults.headers.common.Authorization
    return await apiClient.post('/noRelational', payload, {
      headers: {
        Authorization: token
      }
    })
  },
  async getGDMEntities(payload) {
    const token = axios.defaults.headers.common.Authorization
    return await apiClient.put('/noRelational', payload, {
      headers: {
        Authorization: token
      }
    })
  },
  async getMongoScript() {
    const token = axios.defaults.headers.common.Authorization
    return await apiClient.get('/noRelational', {
      headers: {
        Authorization: token
      }
    })
  }
}
