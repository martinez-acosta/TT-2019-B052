<template>
  <v-app>
    <div>
      <Login />
    </div>
  </v-app>
</template>
<script>
import Login from '@/components/Login.vue'

export default {
  middleware: 'login',
  components: {
    Login
  }
}
</script>

<style></style>
