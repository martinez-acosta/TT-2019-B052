<template>
  <v-content>
    <v-container class="ma-0 pa-0" fluid>
      <v-row dense>
        <v-col>
          <ER :showpallete="false" :readonly="true" />
        </v-col>
        <v-col>
          <div style="background-color:#FF0000;">hola</div>
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
