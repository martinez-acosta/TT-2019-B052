<template>
  <div class="nav">
    <!--El atributo app es para que Vuetify automaticamente se encargue del escalado del elemento-->
    <v-app-bar app color="primary" dense dark collapse-on-scroll flat>
      <v-toolbar-title>TT 2019-B052</v-toolbar-title>
      <v-spacer></v-spacer>
      <template v-if="!loggedIn">
        <v-btn
          v-for="link in links"
          :key="`${link.label}-header-link`"
          text
          rounded
          :to="link.url"
        >
          {{ link.label }}
        </v-btn>
      </template>
      <template v-else>
        <v-btn text rounded :to="links[0].url">
          {{ links[0].label }}
        </v-btn>
        <v-btn text rounded to="/workspace">
          Aplicación
        </v-btn>
        <v-btn text rounded @click="logout">
          Cerrar sesión
        </v-btn>
      </template>
    </v-app-bar>
  </div>
</template>
<!--Recibimos todos los links de layout/default.vue-->
<!--Es el arreglo "links" el props que pasa los links-->
<script>
import { mapGetters } from 'vuex'
export default {
  props: {
    links: {
      type: Array,
      required: true
    }
  },
  computed: {
    ...mapGetters({
      loggedIn: 'calls/loggedIn'
    })
  },
  methods: {
    logout() {
      this.$store.dispatch('calls/logout')
    }
  }
}
</script>

<style></style>
