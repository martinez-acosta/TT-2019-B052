export const state = () => ({
  diagram: null
})
export const mutations = {
  SET_DATA_MODEL(state, dataModel) {
    state.diagram = dataModel.savedModel
  },
  CLEAR_DATA_MODEL() {
    state.diagram = null
    location.reload()
  }
}
export const actions = {
  save({ commit }, dataModel) {
    commit('SET_DATA_MODEL', dataModel)
  },
  clear({ commit }) {
    commit('CLEAR_DATA_MODEL')
  }
}
export const getters = {
  existDiagram(state) {
    return !!state.diagram
  },
  getDiagram(state) {
    return state.diagram
  }
}
