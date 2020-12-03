import Service from '@/services/Service.js'

export const state = () => ({
  diagram: null
})
export const mutations = {
  SET_DATA_MODEL(state, dataModel) {
    state.diagram = dataModel.savedModel
  },
  CLEAR_DATA_MODEL(state) {
    state.diagram = null
    location.reload()
  }
}
export const actions = {
  save({ commit }, dataModel) {
    return Service.saveDiagram(dataModel.savedModel).then((response) => {
      commit('SET_DATA_MODEL', dataModel)
    })
  },
  clear({ commit }) {
    commit('CLEAR_DATA_MODEL')
  },
  getLastDiagram({ commit }) {
    return Service.getLastDiagram()
  },
  validateDiagram({ commit }, diagram) {
    return Service.validateDiagram(diagram)
  },
  convertToSQL({ commit }, payload) {
    return Service.convertToSQL(payload)
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
