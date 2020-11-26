<template>
  <v-container>
    <v-row>
      <v-col cols="10">
        <v-tabs
          v-model="tab"
          background-color="white"
          show-arrows
          flat
          @change="onTabChange"
        >
          <v-tab v-for="n in length" :key="n"> Q{{ n }} </v-tab>
        </v-tabs>
        <v-tabs-items v-model="tab">
          <v-tab-item v-for="n in length" :key="n">
            <Query />
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
import Query from '@/components/Query.vue'
export default {
  components: {
    Query
  },
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
      ],
      // givenEntries: [],
      // findEntries: [],
      currentKey: 0,
      tab: 0
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
  watch: {
    length(val) {
      this.tab = val - 1
    }
  },
  mounted() {
    // Si hay queries en vuex, restaurar estado
    if (this.queries) {
      for (let i = 1; i <= this.queries; i++) {}
    }
  },
  beforeDestroy() {},

  methods: {
    setLength(k) {
      this.$store.dispatch('vuexQueries/setLength', k)
    },
    onTabChange() {
      console.log('Tab change')
    }
  }
}
</script>
