<template>
  <div v-if="!loggedIn">
    <Login />
  </div>
  <div v-else class="text-center">
    <h1>Ya está autenticado.</h1>
  </div>
</template>
<script>
import { mapGetters } from 'vuex'
import Login from '@/components/Login.vue'

export default {
  components: {
    Login
  },
  computed: {
    // loggedIn() {
    // llamada al getter loggedIn que está en store/calls.js
    // return this.$store.getters['calls/loggedIn']
    // }
    ...mapGetters({
      loggedIn: 'calls/loggedIn'
    })
  }
}
</script>

<style></style>
