export const state = () => ({
  queries: '',
  length: 1,
  node: null,
  connectedNode: null,
  nosqlDiagram: null
})

export const mutations = {
  SET_NOSQL_DIAGRAM(state, diagram) {
    state.nosqlDiagram = diagram
  },
  SAVE_QUERIES(state, queries) {
    state.queries = queries
  }
}

export const actions = {
  setNoSQLDiagram({ commit }, diagram) {
    commit('SET_NOSQL_DIAGRAM', diagram)
  },
  saveQueries({ commit }, queries) {
    commit('SAVE_QUERIES', queries)
  }
}

export const getters = {
  getQueries(state) {
    return state.queries
  },
  getNoSQLDiagram(state) {
    return state.nosqlDiagram
  }
}
