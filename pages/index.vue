<template>
  <v-app>
    <v-layout align-center justify-center>
      <div>
        <h1>Welcome to the App!</h1>
        <!--<div v-if="!loggedIn">-->
        <div>
          To use this app you'll need to
          <nuxt-link to="/login">
            Login
          </nuxt-link>
          or
          <nuxt-link to="/register">
            Register
          </nuxt-link>
        </div>
      </div>
    </v-layout>
  </v-app>
</template>

<script>
export default {
  components: {}
}
</script>

<style></style>
