<template>
  <v-app>
    <RegisterUser v-show="!loggedIn" />
  </v-app>
</template>

<script>
import RegisterUser from '@/components/RegisterUser.vue'
export default {
  middleware: 'login',
  components: {
    RegisterUser
  }
}
</script>

<style></style>
