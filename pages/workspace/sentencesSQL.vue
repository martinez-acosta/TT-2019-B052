<template>
  <v-content>
    <sentencesSQL />
  </v-content>
</template>

<script>
import sentencesSQL from '@/components/sentencesSQL'

export default {
  layout: 'workspace',
  components: {
    sentencesSQL
  },
  data() {
    return {}
  },
  methods: {}
}
</script>
