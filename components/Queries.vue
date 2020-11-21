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
            </v-container>
            <!------Fin consultas---------->
          </v-tab-item>
        </v-tabs-items>
      </v-col>
      <!-------Botones------->
      <v-col cols="2">
        <v-tabs>
          <v-btn v-show="length - 1" icon>
            <v-icon @click="length--">mdi-minus</v-icon>
          </v-btn>
          <v-btn icon>
            <v-icon @click="length++">mdi-plus</v-icon>
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
      length: 1,
      tab: 0
    }
  },
  computed: {
    ...mapGetters({
      nodoObtenido: 'vuexQueries/getNode'
    })
  },
  watch: {
    length(val) {
      this.tab = val - 1
    }
  },
  mounted() {
    this.$nuxt.$on('emitGivenValue', () => {
      const nodo = this.nodoObtenido

      this.givenEntries.push({ name: nodo.text, type: 'value' })
    })
  },

  methods: {}
}
</script>
