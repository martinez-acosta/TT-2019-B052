import axios from 'axios'

export const state = () => ({
  user: null
})
export const mutations = {
  SET_USER_DATA(state, userData) {
    state.user = userData
    localStorage.setItem('user', JSON.stringify(userData))
    axios.defaults.headers.common.Authorization = `Bearer ${userData.token}`
  }
}
export const actions = {
  register({ commit }, credentials) {
    return axios
      .post('//localhost:3000/register', credentials)
      .then(({ data }) => {
        commit('SET_USER_DATA', data)
      })
  },
  login({ commit }, credentials) {
    return axios
      .post('//localhost:3000/login', credentials)
      .then(({ data }) => {
        commit('SET_USER_DATA', data)
      })
  }
}
export const getters = {
  loggedIn(state) {
    return !!state.user
  }
}
