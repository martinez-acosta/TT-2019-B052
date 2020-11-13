import Service from '@/services/Service.js'

export const state = () => ({
  user: null
})
export const mutations = {
  SET_USER_DATA(state, userData) {
    state.user = userData
    localStorage.setItem('user', JSON.stringify(userData))
    Service.setToken(userData)
  },
  CLEAR_USER_DATA() {
    localStorage.removeItem('user')
    location.reload()
  }
}
export const actions = {
  register({ commit }, signupInfo) {
    return Service.register(signupInfo).then(({ data }) => {
      commit('SET_USER_DATA', data)
    })
  },
  login({ commit }, credentials) {
    return Service.login(credentials).then(({ data }) => {
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
  },
  userInfo(state) {
    return state.user
  }
}
