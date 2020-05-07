<template>
  <v-app>
    <NavBar />
    <transition name="fade" mode="out-in">
      <nuxt />
    </transition>
    <Footer />
  </v-app>
</template>

<script>
import Footer from '@/components/Footer.vue'
import NavBar from '@/components/workspace/NavBar.vue'
export default {
  components: {
    Footer,
    NavBar
  },
  computed: {},
  methods: {
    logout() {
      this.$store.dispatch('calls/logout')
    }
  },
  middleware: 'authenticated'
}
</script>
