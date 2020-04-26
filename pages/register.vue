<template>
  <v-app>
    <div v-if="!loggedIn">
      <RegisterUser />
    </div>
    <div v-else class="text-center">
      <h1>Ya está autenticado.</h1>
    </div>
  </v-app>
</template>
<script>
import { mapGetters } from 'vuex'
import RegisterUser from '@/components/RegisterUser.vue'
export default {
  components: {
    RegisterUser
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
