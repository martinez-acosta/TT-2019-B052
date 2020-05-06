<template>
  <Diagram v-if="isStripeLoaded"></Diagram>
</template>

<script>
import Diagram from '@/components/Diagram.vue'

export default {
  middleware: 'authenticated',
  layout: 'workspace',
  components: {
    Diagram
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
