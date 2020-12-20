<template>
  <v-content>
    <v-container fluid>
      <v-row>
        <v-col cols="2">
          <!--vacia-->
        </v-col>
        <v-col>
          <SubNavBar />
        </v-col>
        <v-col cols="3">
          <!--vacia-->
        </v-col>
      </v-row>
      <v-row>
        <ER :showpallete="true" />
      </v-row>
    </v-container>
  </v-content>
</template>

<script>
import ER from '@/components/ER.vue'
import SubNavBar from '@/components/SubNavBar.vue'

export default {
  middleware: 'authenticated',
  layout: 'workspace',
  components: {
    ER,
    SubNavBar
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
