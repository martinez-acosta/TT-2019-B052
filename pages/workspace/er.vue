<template>
  <v-content>
    <v-container>
      <v-row>
        <SubNavBar />
      </v-row>
      <v-row>
        <ER />
      </v-row>
    </v-container>
  </v-content>
</template>

<script>
import ER from '@/components/ER.vue'
import SubNavBar from '@/components/SubNavBar.vue'

export default {
  middleware: 'authenticated',
  layout: 'workspace',
  components: {
    ER,
    SubNavBar
  },
  data() {
    return {
      isStripeLoaded: false
    }
  },
  methods: {},
  head() {
    return {}
  }
}
</script>
