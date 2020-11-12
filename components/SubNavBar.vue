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
        <v-divider class="m-0 p-0" vertical></v-divider>
        <v-btn text large color="primary">Validar diagrama</v-btn>
        <v-divider class="mx-4" vertical></v-divider>
        <v-spacer></v-spacer>

        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              icon
              v-bind="attrs"
              v-on="on"
              @click.stop="helpDialog = true"
            >
              <v-icon>mdi-help</v-icon>
            </v-btn>
          </template>
          <span>Ayuda</span>
        </v-tooltip>
      </v-toolbar>
    </v-row>
  </v-container>
</template>

<script>
export default {
  components: {},
  methods: {
    saveModel() {
      this.$nuxt.$emit('saveModel')
    },
    loadModel() {
      this.$nuxt.$emit('loadModel')
    },
    cleanCanvas() {
      this.$nuxt.$emit('cleanCanvas')
    }
  }
}
</script>
<style></style>
