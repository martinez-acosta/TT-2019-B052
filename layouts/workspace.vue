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
    <template v-slot:extension>
      <v-tabs align-with-title>
        <v-tab>Tab 1</v-tab>
        <v-tab>Tab 2</v-tab>
        <v-tab>Tab 3</v-tab>
      </v-tabs>
    </template>
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
  data: () => ({
    items: [
      { title: 'Click Me' },
      { title: 'Click Me' },
      { title: 'Click Me' },
      { title: 'Click Me 2' }
    ]
  }),
  methods: {
    logout() {
      this.$store.dispatch('calls/logout')
    }
  },
  middleware: 'authenticated'
}
</script>
