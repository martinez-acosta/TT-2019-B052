<template>
  <v-container>
    <v-row>
      <v-col cols="10">
        <v-tabs v-model="currentTab" background-color="white" show-arrows flat>
          <v-tab v-for="n in length" :key="n"> Q{{ n }} </v-tab>
        </v-tabs>
        <v-tabs-items :key="componentKey" v-model="currentTab">
          <v-tab-item v-for="n in length" :key="n">
            <!------Consultas---------->
            <v-container>
              <v-row>
                <v-col cols="6">
                  <v-card>
                    <v-card-title>
                      Given
                    </v-card-title>
                    <v-data-table
                      :headers="givenHeaders"
                      hide-default-footer
                      :items="givenEntries[n - 1]"
                    ></v-data-table>
                  </v-card>
                </v-col>
                <v-col cols="6">
                  <v-card>
                    <v-card-title>
                      Find
                    </v-card-title>
                    <v-data-table
                      :headers="findHeaders"
                      hide-default-footer
                      :items="findEntries[n - 1]"
                    ></v-data-table>
                  </v-card>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <textarea
                    style="width:100%;height:300px"
                    :value="diagramaObtenido"
                  >
                  </textarea>
                </v-col>
              </v-row>
            </v-container>
            <!------Fin consultas---------->
          </v-tab-item>
        </v-tabs-items>
      </v-col>
      <!-------Botones------->
      <v-col cols="2">
        <v-tabs>
          <v-btn icon>
            <v-icon @click="setLength(1)">mdi-plus</v-icon>
          </v-btn>
          <v-btn v-show="length - 1" icon>
            <v-icon @click="setLength(-1)">mdi-minus</v-icon>
          </v-btn>
        </v-tabs>
      </v-col>
      <!-------Fin Botones------->
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  data() {
    return {
      componentKey: 0,
      givenHeaders: [
        {
          text: 'Attribute',
          align: 'start',
          sortable: false,
          value: 'name'
        },
        {
          text: '(value/range/set)',
          align: 'start',
          sortable: false,
          value: 'type'
        }
      ],
      findHeaders: [
        {
          text: 'Attribute',
          align: 'start',
          sortable: false,
          value: 'name'
        }
      ],
      // givenEntries: [],
      // findEntries: [],
      currentTab: null,
      tab: null
    }
  },
  computed: {
    ...mapGetters({
      nodoObtenido: 'vuexQueries/getNode',
      nodoConectado: 'vuexQueries/getConnectedNode',
      diagramaObtenido: 'vuexER/getDiagram',
      length: 'vuexQueries/getLength',
      queries: 'vuexQueries/getQueries',
      givenEntries: 'vuexQueries/getGivenEntries',
      findEntries: 'vuexQueries/getFindEntries'
    })
  },
  watch: {},
  mounted() {
    // listeners
    this.$nuxt.$on('emitGivenValue', () => {
      const nodo = this.nodoObtenido
      const nodoConectado = this.nodoConectado

      this.$store
        .dispatch('vuexQueries/pushGivenEntry', {
          name: nodoConectado.text + '.' + nodo.text,
          type: 'value',
          tab: this.currentTab,
          nodo: this.nodoObtenido,
          nodoConectado: this.nodoConectado
        })
        .then(this.forceRerender())
    })

    this.$nuxt.$on('emitGivenRange', () => {
      const nodo = this.nodoObtenido
      const nodoConectado = this.nodoConectado

      this.$store
        .dispatch('vuexQueries/pushGivenEntry', {
          name: nodoConectado.text + '.' + nodo.text,
          type: 'range',
          tab: this.currentTab,
          nodo: this.nodoObtenido,
          nodoConectado: this.nodoConectado
        })
        .then(this.forceRerender())
    })

    this.$nuxt.$on('emitGivenSet', () => {
      const nodo = this.nodoObtenido
      const nodoConectado = this.nodoConectado

      this.$store
        .dispatch('vuexQueries/pushGivenEntry', {
          name: nodoConectado.text + '.' + nodo.text,
          type: 'set',
          tab: this.currentTab,
          nodo: this.nodoObtenido,
          nodoConectado: this.nodoConectado
        })
        .then(this.forceRerender())
    })

    this.$nuxt.$on('emitFindValue', () => {
      const nodo = this.nodoObtenido
      const nodoConectado = this.nodoConectado

      this.$store
        .dispatch('vuexQueries/pushFindEntry', {
          name: nodoConectado.text + '.' + nodo.text,
          type: 'value',
          tab: this.currentTab,
          nodo: this.nodoObtenido,
          nodoConectado: this.nodoConectado
        })
        .then(this.forceRerender())
    })
  },
  beforeDestroy() {
    this.$nuxt.$off('emitGivenValue')
    this.$nuxt.$off('emitGivenRange')
    this.$nuxt.$off('emitGivenSet')
    this.$nuxt.$off('emitFindValue')
  },

  methods: {
    setLength(k) {
      this.$store
        .dispatch('vuexQueries/setLength', k)
        .then(this.$store.dispatch('vuexQueries/setArraySize'))
    },
    forceRerender() {
      this.componentKey += 1
    }
  }
}
</script>
