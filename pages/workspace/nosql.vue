<template>
  <v-content>
    <v-container fluid>
      <v-row>
        <NoSQL />
      </v-row>
    </v-container>
  </v-content>
</template>

<script>
import NoSQL from '@/components/NoSQL.vue'

export default {
  middleware: 'authenticated',
  layout: 'workspace',
  components: {
    NoSQL
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
