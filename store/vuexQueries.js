export const state = () => ({
  queries: 0,
  givenEntries: [],
  findEntries: [],
  length: 1,
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
  ADD_QUERY(state) {
    state.queries++
  },
  SET_LENGTH(state, k) {
    state.length += k
  }
}

export const actions = {
  pushNode({ commit }, node) {
    commit('PUSH_NODE', node)
  },
  pushConnectedNode({ commit }, connectedNode) {
    commit('PUSH_CONNECTED_NODE', connectedNode)
  },
  addQuery({ commit }) {
    commit('ADD_QUERY')
  },
  setLength({ commit }, k) {
    commit('SET_LENGTH', k)
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
  },
  getLength(state) {
    return state.length
  },
  getGivenEntries(state) {
    return state.givenEntries
  },
  getFindEntries(state) {
    return state.findEntries
  }
}
