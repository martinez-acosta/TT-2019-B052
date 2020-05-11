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
    return {}
  },
  methods: {},
  head() {
    return {}
  }
}
</script>
