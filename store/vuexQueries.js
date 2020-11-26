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
  PUSH_GIVEN_ENTRY(state, givenEntry) {
    console.log(givenEntry)
    state.givenEntries[givenEntry.tab].push({
      name: givenEntry.name,
      type: givenEntry.type
    })
  },
  SET_LENGTH(state, k) {
    state.length += k
  },
  SET_ARRAY_SIZE(state) {
    // Si el tam del array es menor al número de preguntas, creamos las entradas faltantes
    // if (state.givenEntries.length < state.length) {
    //   for (let i=state.givenEntries.length; i < state.length; i++){
    //     state.givenEntries.push([])
    //   }
    // }
    state.givenEntries.length = state.length
    for (let i = 0; i < state.givenEntries.length; i++) {
      if (typeof state.givenEntries[i] === 'undefined') {
        state.givenEntries[i] = []
      }
    }
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
  pushGivenEntry({ commit }, givenEntry) {
    commit('PUSH_GIVEN_ENTRY', givenEntry)
  },
  setLength({ commit }, k) {
    commit('SET_LENGTH', k)
  },
  setArraySize({ commit }, n) {
    commit('SET_ARRAY_SIZE', n)
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
