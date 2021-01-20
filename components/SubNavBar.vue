<template>
  <v-container fill-height fluid ma-0 pa-0>
    <v-row>
      <v-toolbar dense>
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn icon v-bind="attrs" v-on="on" @click="saveModel()">
              <v-icon>mdi-content-save</v-icon>
            </v-btn>
          </template>
          <span>Guardar</span>
        </v-tooltip>

        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn icon v-bind="attrs" v-on="on" @click="loadModel()">
              <v-icon>mdi-folder-open</v-icon>
            </v-btn>
          </template>
          <span>Abrir...</span>
        </v-tooltip>
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn icon v-bind="attrs" v-on="on" @click="cleanCanvas()">
              <v-icon>mdi-file</v-icon>
            </v-btn>
          </template>
          <span>Nuevo</span>
        </v-tooltip>
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn icon v-bind="attrs" v-on="on" @click="onButtonClick">
              <v-icon left>
                mdi-upload
              </v-icon>
            </v-btn>
            <input
              ref="uploader"
              class="d-none"
              type="file"
              accept="application/JSON"
              @change="onFileChanged"
            />
          </template>
          <span>Cargar...</span>
        </v-tooltip>
        <v-divider class="m-0 p-0" vertical></v-divider>
        <v-btn text large color="primary" @click="validateDiagram()">
          Validar diagrama
        </v-btn>
        <v-divider class="mx-4" vertical></v-divider>
        <v-spacer></v-spacer>
      </v-toolbar>
    </v-row>
  </v-container>
</template>

<script>
export default {
  components: {},
  data() {
    return {
      diagramFromFile: null
    }
  },
  methods: {
    saveModel() {
      this.$nuxt.$emit('axiosSaveModel')
    },
    loadModel() {
      this.$nuxt.$emit('axiosLoadModel')
    },
    cleanCanvas() {
      this.$nuxt.$emit('cleanCanvas')
    },
    validateDiagram() {
      this.$nuxt.$emit('validateDiagram')
    },
    onButtonClick() {
      this.$refs.uploader.click()
    },
    onFileChanged(e) {
      const that = this
      const reader = new FileReader()
      reader.onload = function(event) {
        const jsonObj = JSON.parse(event.target.result)
        if (
          'nodeDataArray' in jsonObj &&
          'linkDataArray' in jsonObj &&
          'class' in jsonObj &&
          'modelData' in jsonObj
        ) {
          // llamada a funciona para cargar diagrama en vuex
          that.diagramFromFile = jsonObj
          that.loadModelFromFile()
        } else {
          // Lanzar snotify error
          console.log('Archivo no valido')
        }
      }
      reader.readAsText(e.target.files[0]) // do something
    },
    loadModelFromFile() {
      const diagram = this.diagramFromFile
      if (diagram.nodeDataArray && diagram.linkDataArray) {
        this.$nuxt.$emit('LoadModelFromFile', this.diagramFromFile)
      } else {
        // lanzar snotify warning
        console.log('diagrma con nodos o links vacios')
      }
    }
  }
}
</script>
<style></style>
