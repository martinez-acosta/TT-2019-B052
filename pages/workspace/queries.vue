<template>
  <v-content>
    <v-container class="ma-0 pa-0">
      <v-row no-gutters align-self="start">
        <v-col cols="8">
          <ER :showpallete="false" :readonly="false" />
        </v-col>
        <v-col>
          <div>Hola</div>
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
