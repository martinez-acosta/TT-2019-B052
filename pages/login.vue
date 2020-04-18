<template>
  <div>
    <Login />
  </div>
</template>
<script>
import Login from '@/components/Login.vue'
export default {
  components: {
    Login
  },
  head() {
    return {
      title: 'login',
      meta: [
        {
          hid: 'description',
          name: 'description',
          content:
            'Where you can find all the events taking place in your neighborhood'
        }
      ]
    }
  }
}
</script>

<style></style>
