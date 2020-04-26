<template>
  <v-app>
    <v-layout align-center justify-center>
      <div>
        <h1 class="text-center">¡Bienvenido!</h1>
        <div v-if="!loggedIn">
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
export default {
  computed: {
    loggedIn() {
      // llamada al getter loggedIn que está en store/calls.js
      return this.$store.getters['calls/loggedIn']
    }
  }
}
</script>

<style></style>
