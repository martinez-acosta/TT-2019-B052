<template>
  <v-container fluid>
    <client-only>
      <vue-snotify></vue-snotify>
    </client-only>
    <div class="row col">
      <v-toolbar dense>
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              icon
              v-bind="attrs"
              :download="scriptName"
              :href="urlFile"
              v-on="on"
              @click="downloadScript()"
            >
              <v-icon>mdi-download</v-icon>
            </v-btn>
          </template>
          <span>Descargar</span>
        </v-tooltip>

        <v-divider class="m-0 p-0" vertical></v-divider>
        <v-btn text large color="primary" @click="convertToSQLDialog = true">
          Obtener Sentencias SQL
        </v-btn>
        <v-divider class="mx-4" vertical></v-divider>
      </v-toolbar>
    </div>

    <div
      class="container-fluid"
      style="width: 100%; height: 70%; overflow: auto;"
    >
      <ssh-pre
        language="sql"
        label="SQL"
        :reactive="true"
        :copy-button="true"
        :dark="false"
      >
        {{ sentences }}
      </ssh-pre>
    </div>

    <!-- Dialog/modals -->
    <v-dialog v-model="helpDialog" max-width="360">
      <v-card>
        <v-card-title class="headline"
          >Sentencias SQL equivalentes al diagrama ER</v-card-title
        >

        <v-card-text>
          En este apartado puede observar las sentencias SQL equivalentes al
          diagrama entidad-relación generado en el paso 1. <br />
          Puede copiar o descargar estas sentencias para comprobar su correcto
          funcionamiento en el gestor de base de datos MySQL.
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="helpDialog = false"
            >De acuerdo</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="convertToSQLDialog" max-width="360">
      <v-card>
        <v-card-title class="headline">Obtener las Sentencias SQL</v-card-title>

        <v-card-text>
          <v-text-field
            v-model="db_name"
            label="nombre de la base de datos"
            required
          ></v-text-field>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="getSentencesSQL()"
            >enviar</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script type="module">
import SshPre from 'simple-syntax-highlighter'
import 'simple-syntax-highlighter/dist/sshpre.css'
import { mapGetters } from 'vuex'

export default {
  components: { SshPre },
  data() {
    return {
      scriptName: '',
      urlFile: '#',
      db_name: '',
      helpDialog: false,
      convertToSQLDialog: false,
      sentences: `
CREATE DATABASE IF NOT EXISTS 'example';

USE 'example';

/*Table structure for table 'customers' */

DROP TABLE IF EXISTS 'table_name';

CREATE TABLE 'customers' (
  'attribute' int(11) NOT NULL,
  
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
`
    }
  },
  computed: {
    ...mapGetters({
      currentDiagram: 'vuexER/getDiagram'
    })
  },
  methods: {
    getSentencesSQL() {
      const diagram = this.currentDiagram
      this.$nuxt.$loading.start()

      this.$store
        .dispatch('axiosER/convertToSQL', {
          diagram,
          dbName: this.db_name
        })
        .then((response) => {
          this.$nuxt.$loading.finish()

          this.sentences = response.data
        })
        .catch((error) => {
          this.$nuxt.$loading.fail()
          this.$nuxt.$loading.finish()
          if (error.response.status === 500) {
            this.$snotify.warning(
              '¡Algo ocurrió! No fue posible obtener las sentencias SQ del diagrama, intente más tarde.'
            )
          }
        })
      this.convertToSQLDialog = false
    },
    downloadScript() {
      const scriptData = encodeURIComponent(this.sentences)
      this.urlFile = `data:text/plain;charset=utf-8,${scriptData}` // application/sql
      const dbname = this.db_name ? this.db_name : 'tt2019-B052'
      this.scriptName = dbname + '.sql'
      this.$snotify.success('Archivo descargado. ')
    }
  }
}
</script>
