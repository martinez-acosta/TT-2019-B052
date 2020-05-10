<template>
  <v-content>
    <DiagramER />
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
    return {}
  }
}
</script>
