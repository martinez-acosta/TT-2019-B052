export const state = () => ({
  queries: [],
  node: null
})

export const mutations = {
  PUSH_NODE(state, node) {
    state.node = node
  },
  PUSH_QUERY(state, query) {
    state.queries.push(query)
  }
}

export const actions = {
  pushNode({ commit }, node) {
    commit('PUSH_NODE', node)
  },
  pushQuery({ commit }, query) {
    commit('PUSH_QUERY', query)
  }
}

export const getters = {
  getNode(state) {
    return state.node
  },
  getQueries(state) {
    return state.queries
  }
}
