<template>
  <v-container fluid>
    <client-only>
      <vue-snotify></vue-snotify>
    </client-only>
    <!------Consultas---------->
    <v-row>
      <v-btn
        block
        color="success"
        :disabled="!enableBtnQueries"
        @click="getNoSQLDiagram"
        >Obtener Modelo NoSQL</v-btn
      >
    </v-row>
    <v-row>
      <v-col cols="6">
        <div style="width: 100%; height: 70%; overflow: auto; font-size: 12px;">
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
        <v-card-title>Consultas modelo GDM</v-card-title>
        <v-textarea
          id="queriesGDM"
          v-model="gdmQueries"
          outlined
          rows="24"
          label="Consultas de accesso"
          style="font-size: 12px;"
        >
        </v-textarea>
      </v-col>
    </v-row>
    <!------Fin consultas---------->
    <!-- Dialog/modals -->
    <v-dialog v-model="validDiagram" scrollable min-width="450" max-width="600">
      <v-card>
        <v-card-title class="headline">
          Transformación al modelo No SQL
        </v-card-title>
        <v-card-text font-size="24px">
          La Tranformación fue exitosa, presione continuar para visualizar el
          diagrama.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn left color="success" to="/workspace/nosql">
            Continuar
          </v-btn>
          <v-btn color="primary" @click="validDiagram = false">
            Cerrar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
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
      entitiesER: ``,
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
      gdmQueries: '',
      nosqlDiagram: '',
      validDiagram: false
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
    }),
    enableBtnQueries() {
      return Boolean(this.gdmQueries)
    }
  },
  watch: {},
  created() {},
  mounted() {
    this.getEntitiesGdm()
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
    },
    getNoSQLDiagram() {
      if (this.gdmQueries.length < 50) {
        this.$snotify.warning(
          'Las consultas de acceso no pueden ser tan cortas.'
        )
      } else {
        this.$store
          .dispatch('axiosNoSQL/getNoSQLDiagram', {
            entities: this.entitiesER,
            queries: this.gdmQueries
          })
          .then((response) => {
            this.validDiagram = true
            const diagram = response.data.diagram
            this.$store.dispatch('vuexQueries/setNoSQLDiagram', diagram)
          })
          .catch(() => {
            const msg =
              'Ocurrio un error durante la trandormación, revise las consultas.'
            this.$snotify.error(msg)
          })
      }
    },
    getEntitiesGdm() {
      const diagram = JSON.parse(this.diagramaObtenido)
      if (
        diagram.nodeDataArray.length === 0 ||
        diagram.linkDataArray.length === 0
      ) {
        this.$snotify.warning(
          'No se encontro un diagrama en el contexto de la aplicación.'
        )
      } else {
        this.$store
          .dispatch('axiosNoSQL/getGDMEntities', {
            diagram: this.diagramaObtenido
          })
          .then((response) => {
            const nosqlRawDiagram = response.data
            this.entitiesER = '\n' + nosqlRawDiagram
          })
          .catch(() => {
            const msg =
              'Ocurrio un error al obtener las entidades del diagrama ER, revise las consultas.'
            this.$snotify.error(msg)
          })
      }
    }
  }
}
</script>
