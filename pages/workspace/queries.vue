<template>
  <v-content>
    <v-container class="ma-0 pa-0" fluid>
      <v-row no-gutters>
        <v-col cols="7">
          <ER :showpallete="false" :readonly="true" />
        </v-col>
        <v-col>
          <Queries />
        </v-col>
      </v-row>
    </v-container>
  </v-content>
</template>

<script>
import ER from '@/components/ER.vue'
import Queries from '@/components/Queries.vue'
export default {
  middleware: 'authenticated',
  layout: 'workspace',
  components: {
    ER,
    Queries
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
