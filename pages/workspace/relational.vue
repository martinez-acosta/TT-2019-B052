<template>
  <v-content>
    <DiagramRelational />
  </v-content>
</template>

<script>
import DiagramRelational from '@/components/DiagramRelational.vue'

export default {
  middleware: 'authenticated',
  layout: 'workspace',
  components: {
    DiagramRelational
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
