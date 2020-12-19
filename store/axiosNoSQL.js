import Service from '@/services/Service.js'

export const actions = {
  getNoSQLDiagram({ commit }, payload) {
    return Service.getNoSQLDiagram(payload)
  }
}
