import axios from 'axios'

export const state = () => ({
  user: null
})
export const mutations = {
  SET_USER_DATA(state, userData) {
    state.user = userData
    localStorage.setItem('user', JSON.stringify(userData))
    axios.defaults.headers.common.Authorization = `Bearer ${userData.token}`
    state.logged = !!state.user
  },
  CLEAR_USER_DATA() {
    localStorage.removeItem('user')
    state.logged = false
    location.reload()
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
  },
  logout({ commit }) {
    commit('CLEAR_USER_DATA')
  },
  nuxtClientInit({ commit }, { req }) {
    const userString = localStorage.getItem('user') // grab user data from local storage
    if (userString) {
      // check to see if there is indeed a user
      const userData = JSON.parse(userString) // parse user data into JSON
      commit('SET_USER_DATA', userData) // restore user data with Vuex
    }
  }
}
export const getters = {
  loggedIn(state) {
    return !!state.user
  }
}
