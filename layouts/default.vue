<template>
  <v-app>
    <div id="app">
      <NavBar :links="links" />
      <v-content>
        <nuxt />
        <!--Aquí es donde los elementos de Nuxtjs son renderizados (las pages) -->
      </v-content>
      <Footer />
    </div>
  </v-app>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
import Footer from '@/components/Footer.vue'

export default {
  components: {
    NavBar,
    Footer
  },
  data() {
    return {
      links: [
        { label: 'Home', url: '/' },
        { label: 'Login', url: '/login' }
      ]
    }
  },
  head() {
    return {
      titleTemplate: '%s - TT 2019-B052',
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
