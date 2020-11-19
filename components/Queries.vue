<template>
  <v-card>
    <v-tabs v-model="tab" background-color="blue darken-3" dark show-arrows>
      <v-tab v-for="n in length" :key="n"> Q{{ n }} </v-tab>
      <v-btn icon>
        <v-icon @click="length++">mdi-plus</v-icon>
      </v-btn>
    </v-tabs>
    <!--<v-card-text class=">
      <v-btn :disabled="!length" text @click="length--">
        Remove Query
      </v-btn>
      <v-divider class="mx-4" vertical></v-divider>
      <v-btn text @click="length++">
        Add Query
      </v-btn>
    </v-card-text>-->
  </v-card>
</template>

<script>
export default {
  data: () => ({
    length: 1,
    tab: null
  }),

  watch: {
    length(val) {
      this.tab = val - 1
    }
  }
}
</script>
