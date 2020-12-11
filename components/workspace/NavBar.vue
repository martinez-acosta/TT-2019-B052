<template>
  <v-app-bar app color="primary" dark clipped-right clipped-left dense flat>
    <v-toolbar-title>{{ user.name }}</v-toolbar-title>

    <v-divider class="mx-4" inset vertical></v-divider>
    <span class="subheading">{{ user.email }}</span>
    <v-spacer></v-spacer>
    <v-btn text @click="logout">
      Cerrar sesión
    </v-btn>

    <template v-slot:extension>
      <v-tabs align-with-title>
        <v-tabs-slider color="yellow"></v-tabs-slider>

        <v-tab nuxt to="/workspace/er">1: Diagrama ER</v-tab>
        <v-tab nuxt to="/workspace/queries">2: Consultas</v-tab>
        <v-tab nuxt to="/workspace/sentencesSQL">3: Sentencias SQL</v-tab>
        <v-tab nuxt to="/workspace/nosql">4: Modelo NoSQL</v-tab>
      </v-tabs>
    </template>
  </v-app-bar>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  computed: {
    ...mapGetters({
      loggedIn: 'calls/loggedIn',
      user: 'calls/userInfo'
    })
  },
  methods: {
    logout() {
      this.$store.dispatch('calls/logout')
    }
  }
}
</script>
