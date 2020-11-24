<template>
  <v-container>
    <v-row>
      <v-col cols="10">
        <v-tabs v-model="tab" background-color="white" show-arrows flat>
          <v-tab v-for="n in length" :key="n"> Q{{ n }} </v-tab>
        </v-tabs>
        <v-tabs-items v-model="tab">
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
        <!-- <v-tabs>
          <v-btn v-show="length - 1" icon>
            <v-icon @click="length--">mdi-minus</v-icon>
          </v-btn>
          <v-btn icon>
            <v-icon @click="length++">mdi-plus</v-icon>
          </v-btn>
        </v-tabs> -->
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
      givenEntries: [],
      findHeaders: [
        {
          text: 'Attribute',
          align: 'start',
          sortable: false,
          value: 'name'
        }
      ],
      findEntries: [],
      // length: 1,
      tab: 0,
      myDiagram: ''
    }
  },
  computed: {
    ...mapGetters({
      nodoObtenido: 'vuexQueries/getNode',
      nodoConectado: 'vuexQueries/getConnectedNode',
      diagramaObtenido: 'vuexER/getDiagram',
      length: 'vuexQueries/getLength'
    })
  },
  watch: {
    length(val) {
      this.tab = val - 1
    }
  },
  mounted() {
    // Ibtener
    this.$nuxt.$on('emitGivenValue', () => {
      const nodo = this.nodoObtenido
      const nodoConectado = this.nodoConectado

      this.givenEntries.push({
        name: nodoConectado.text + '.' + nodo.text,
        type: 'value'
      })
    })
    this.$nuxt.$on('emitGivenRange', () => {
      const nodo = this.nodoObtenido
      const nodoConectado = this.nodoConectado

      this.givenEntries.push({
        name: nodoConectado.text + '.' + nodo.text,
        type: 'range'
      })
    })
    this.$nuxt.$on('emitGivenSet', () => {
      const nodo = this.nodoObtenido
      const nodoConectado = this.nodoConectado

      this.givenEntries.push({
        name: nodoConectado.text + '.' + nodo.text,
        type: 'set'
      })
    })
    this.$nuxt.$on('emitFindValue', () => {
      const nodo = this.nodoObtenido
      const nodoConectado = this.nodoConectado

      this.findEntries.push({
        name: nodoConectado.text + '.' + nodo.text,
        type: 'value'
      })
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
      this.$store.dispatch('vuexQueries/setLength', k)
    }
  }
}
</script>
