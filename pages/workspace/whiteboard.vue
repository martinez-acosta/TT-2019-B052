<template>
  <div id="app">
    <Diagram></Diagram>
  </div>
</template>

<script>
import Diagram from '@/components/Diagram.vue'

export default {
  middleware: 'authenticated',
  layout: 'workspace',
  components: {
    Diagram
  },
  methods: {}
}
</script>
