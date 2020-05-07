<template>
  <v-content>
    <DiagramER v-if="isStripeLoaded" />
  </v-content>
</template>

<script>
import DiagramER from '@/components/DiagramER.vue'

export default {
  middleware: 'authenticated',
  layout: 'workspace',
  components: {
    DiagramER
  },
  data() {
    return {
      isStripeLoaded: false
    }
  },
  methods: {},
  head() {
    return {
      script: [
        {
          src: '/Figures.js',
          defer: true,
          // Changed after script load
          callback: () => {
            this.isStripeLoaded = true
          }
        }
      ]
    }
  }
}
</script>
