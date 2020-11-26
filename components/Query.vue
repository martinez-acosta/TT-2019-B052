<template>
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
            :items="givenEntries"
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
            :items="findEntries"
          ></v-data-table>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  data() {
    return {
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
      ]
      // givenEntries: [],
      // findEntries: [],
    }
  },
  computed: {
    ...mapGetters({
      nodoObtenido: 'vuexQueries/getNode',
      nodoConectado: 'vuexQueries/getConnectedNode',
      // diagramaObtenido: 'vuexER/getDiagram',
      // length: 'vuexQueries/getLength',
      // queries: 'vuexQueries/getQueries',
      givenEntries: 'vuexQueries/getGivenEntries',
      findEntries: 'vuexQueries/getFindEntries'
    })
  },
  watch: {
    length(val) {
      this.tab = val - 1
    }
  },
  mounted() {
    console.log('Hola')
    // listeners
    this.$nuxt.$on('emitGivenValue', () => {
      const nodo = this.nodoObtenido
      const nodoConectado = this.nodoConectado

      this.givenEntries.push({
        name: nodoConectado.text + '.' + nodo.text,
        type: 'value'
      })
    })
    // this.$nuxt.$on('emitGivenRange', () => {
    //   const nodo = this.nodoObtenido
    //   const nodoConectado = this.nodoConectado

    //   this.givenEntries.push({
    //     name: nodoConectado.text + '.' + nodo.text,
    //     type: 'range'
    //   })
    // })
    // this.$nuxt.$on('emitGivenSet', () => {
    //   const nodo = this.nodoObtenido
    //   const nodoConectado = this.nodoConectado

    //   this.givenEntries.push({
    //     name: nodoConectado.text + '.' + nodo.text,
    //     type: 'set'
    //   })
    // })
    // this.$nuxt.$on('emitFindValue', () => {
    //   const nodo = this.nodoObtenido
    //   const nodoConectado = this.nodoConectado

    //   this.findEntries.push({
    //     name: nodoConectado.text + '.' + nodo.text,
    //     type: 'value'
    //   })
    // })
  },
  beforeDestroy() {
    this.$nuxt.$off('emitGivenValue')
    this.$nuxt.$off('emitGivenRange')
    this.$nuxt.$off('emitGivenSet')
    this.$nuxt.$off('emitFindValue')
  },

  methods: {}
}
</script>
