<template>
  <v-container>
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
      <v-col cols="4">
        <div style="width: 100%; height: 67%; overflow: auto; font-size: 12px;">
          <ssh-pre
            language="pug"
            label="Entidades del GDM"
            :reactive="true"
            :copy-button="false"
            :dark="false"
          >
            {{ entitiesER }}
          </ssh-pre>
        </div>
      </v-col>
      <v-col>
        <v-textarea
          id="queriesGDM"
          v-model="gdmQueries"
          outlined
          rows="23"
          label="Consultas del GDM"
          style="font-size: 12px;"
        >
        </v-textarea>

        <!--<div style="width: 100%; height: 50%; overflow: auto; font-size: 12px;">
          
        </div>-->
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
import '@/static/ssh-gdm.css'

export default {
  components: {
    SshPre
  },
  data() {
    return {
      componentKey: 0,
      entitiesER: ``,
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
    this.gdmQueries = this.queries
    this.getEntitiesGdm()
  },
  beforeDestroy() {
    this.vuexSaveQueries()
  },

  methods: {
    forceRerender() {
      this.componentKey += 1
    },
    vuexSaveQueries() {
      this.$store.dispatch('vuexQueries/saveQueries', this.gdmQueries)
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
      if (!diagram) {
        return
      }
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
