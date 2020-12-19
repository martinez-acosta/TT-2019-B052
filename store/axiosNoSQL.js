import Service from '@/services/Service.js'

export const actions = {
  getNoSQLDiagram({ commit }, payload) {
    return Service.getNoSQLDiagram(payload)
  },
  getGDMEntities({ commit }, payload) {
    return Service.getGDMEntities(payload)
  }
}
