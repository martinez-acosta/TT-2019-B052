<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-tabs v-model="currentTab" background-color="white" show-arrows flat>
          <v-tab v-for="n in length" :key="n"> Q{{ n }} </v-tab>
        </v-tabs>
        <v-tabs-items :key="componentKey" v-model="currentTab">
          <v-tab-item v-for="n in length" :key="n">
            <!------Consultas---------->
            <v-container>
              <!-- <v-row>
                <v-col cols="6">
                  <v-card>
                    <v-card-title>
                      Respecto a:
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
                      Encontrar:
                    </v-card-title>
                    <v-data-table
                      :headers="findHeaders"
                      hide-default-footer
                      :items="findEntries[n - 1]"
                    ></v-data-table>
                  </v-card>
                </v-col>
              </v-row> -->
              <v-row>
                <v-col cols="6">
                  <div class="overflow-auto" style="overflow: auto;">
                    <ssh-pre
                      language="pug"
                      label="entidades del GDM"
                      :reactive="true"
                      :copy-button="false"
                      :dark="false"
                    >
                      {{ entitiesER }}
                    </ssh-pre>
                  </div>
                </v-col>
                <v-col cols="6">
                  <p>Agrega tus consulta para el modelo GDM</p>
                  <v-textarea
                    id="queriesGDM"
                    outlined
                    label="Consultas de accesso"
                  >
                  </v-textarea>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <v-btn block color="success"
                    >Obtener Modelo NoSQL</v-btn
                  ></v-col
                >
              </v-row>
            </v-container>
            <!------Fin consultas---------->
          </v-tab-item>
        </v-tabs-items>
      </v-col>
      <!-------Botones------->
      <!-- <v-col cols="2">
        <v-tabs>
          <v-btn icon>
            <v-icon @click="setLength(1)">mdi-plus</v-icon>
          </v-btn>
          <v-btn v-show="length - 1" icon>
            <v-icon @click="setLength(-1)">mdi-minus</v-icon>
          </v-btn>
        </v-tabs>
      </v-col> -->
      <!-------Fin Botones------->
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
import SshPre from 'simple-syntax-highlighter'
import 'simple-syntax-highlighter/dist/sshpre.css'

export default {
  components: {
    SshPre
  },
  data() {
    return {
      componentKey: 0,
      givenHeaders: [
        {
          text: 'Atributo',
          align: 'start',
          sortable: false,
          value: 'name'
        },
        {
          text: 'Valor',
          align: 'start',
          sortable: false,
          value: 'type'
        }
      ],
      entitiesER: `
entity User {
  id userId unique
  text userName
  text userEmail
  text[*] areasOfExpertise
  ref Review[*] reviews
  ref Artifact[*] likesArtifacts
  ref Venue[*] likesVenue
}

entity Venue {
  id venueId unique
  text venueName
  number year
  text country
  text homepage
  text[*] topics
  ref Artifact[*] artifacts
}

entity Artifact {
  id artifactId unique
  text artifactTitle
  text[*] authors
  text[*] keywords
  number numRatings
  number sumRatings
  number avgRating
  ref Venue[1] venue
}

entity Review {
  id reviewId unique
  text reviewTitle
  text body
  number rating
  ref Artifact[1] artifact
}`,
      findHeaders: [
        {
          text: 'Atributo',
          align: 'start',
          sortable: false,
          value: 'name'
        }
      ],
      // givenEntries: [],
      // findEntries: [],
      currentTab: null,
      tab: null,
      aliasEntity: 'alias'
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

    this.$nuxt.$on('emitAliasEntity', () => {
      const nodo = this.nodoObtenido
      console.log(nodo)
    })
  },
  beforeDestroy() {
    this.$nuxt.$off('emitGivenValue')
    this.$nuxt.$off('emitGivenRange')
    this.$nuxt.$off('emitGivenSet')
    this.$nuxt.$off('emitFindValue')
    this.$nuxt.$off('emitAliasEntity')
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
