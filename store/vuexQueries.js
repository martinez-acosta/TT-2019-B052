export const state = () => ({
  queries: [],
  node: null,
  connectedNode: null
})

export const mutations = {
  PUSH_NODE(state, node) {
    state.node = node
  },

  PUSH_CONNECTED_NODE(state, connectedNode) {
    state.connectedNode = connectedNode
  },
  PUSH_QUERY(state, query) {
    state.queries.push(query)
  }
}

export const actions = {
  pushNode({ commit }, node) {
    commit('PUSH_NODE', node)
  },
  pushConnectedNode({ commit }, connectedNode) {
    commit('PUSH_CONNECTED_NODE', connectedNode)
  },
  pushQuery({ commit }, query) {
    commit('PUSH_QUERY', query)
  }
}

export const getters = {
  getNode(state) {
    return state.node
  },
  getConnectedNode(state) {
    return state.connectedNode
  },
  getQueries(state) {
    return state.queries
  }
}
