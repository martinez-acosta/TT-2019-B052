<template>
  <v-content>
    <v-container>
      <v-row no-gutters align-self="start">
        <v-col>
          <ER :showpallete="false" :readonly="false" />
        </v-col>
      </v-row>
    </v-container>
  </v-content>
</template>

<script>
import ER from '@/components/ER.vue'

export default {
  middleware: 'authenticated',
  layout: 'workspace',
  components: {
    ER
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
