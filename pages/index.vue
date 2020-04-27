<template>
  <v-app>
    <v-layout align-center justify-center>
      <div>
        <h1 class="text-center">¡Bienvenido!</h1>
        <div v-show="!loggedIn">
          Para usar esta aplicación tienes que
          <nuxt-link to="/login">
            iniciar sesión
          </nuxt-link>
          o
          <nuxt-link to="/register">
            registrarte
          </nuxt-link>
        </div>
      </div>
    </v-layout>
  </v-app>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  computed: {
    ...mapGetters({
      loggedIn: 'calls/loggedIn'
    })
  }
}
</script>

<style></style>
