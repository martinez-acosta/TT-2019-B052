<template>
  <v-content>
    <v-container class="ma-0 pa-0" fluid>
      <v-row dense align-self="start">
        <v-col>
          <ER :showpallete="false" :readonly="false" />
        </v-col>
        <v-col>
          <div>hola</div>
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
