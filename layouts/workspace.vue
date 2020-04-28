<template>
  <v-app id="inspire">
    <v-app-bar app clipped-right clipped-left color="primary" dense dark>
      <v-toolbar-title>TT 2019-B052</v-toolbar-title>
      <v-spacer />
      <v-btn text rounded @click="logout">
        Logout
      </v-btn>
    </v-app-bar>

    <NavDrawLeft />

    <v-content>
      <v-container class="fill-height" fluid>
        <v-row justify="center" align="center">
          <v-col class="shrink">
            <transition name="fade" mode="out-in">
              <nuxt />
            </transition>
          </v-col>
        </v-row>
      </v-container>
    </v-content>

    <Footer />
  </v-app>
</template>

<script>
import Footer from '@/components/Footer.vue'
import NavDrawLeft from '@/components/NavDrawLeft.vue'
export default {
  components: {
    Footer,
    NavDrawLeft
  },
  data: () => ({}),
  methods: {
    logout() {
      this.$store.dispatch('calls/logout')
    }
  },
  middleware: 'authenticated'
}
</script>
