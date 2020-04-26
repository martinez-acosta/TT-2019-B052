<template>
  <v-app>
    <div>
      <RegisterUser />
    </div>
  </v-app>
</template>
<script>
import RegisterUser from '@/components/RegisterUser.vue'
export default {
  components: {
    RegisterUser
  },
  middleware: 'authLogin'
}
</script>

<style></style>
