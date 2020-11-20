<template>
  <v-container>
    <v-row>
      <v-col cols="10">
        <v-tabs v-model="tab" background-color="white" show-arrows flat>
          <v-tab v-for="n in length" :key="n"> Q{{ n }} </v-tab>
        </v-tabs>
      </v-col>
      <v-col cols="2">
        <v-tabs>
          <v-btn v-show="length - 1" icon>
            <v-icon @click="length--">mdi-minus</v-icon>
          </v-btn>
          <v-btn icon>
            <v-icon @click="length++">mdi-plus</v-icon>
          </v-btn>
        </v-tabs>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      length: 1,
      tab: null
    }
  },
  watch: {
    length(val) {
      this.tab = val - 1
    }
  },
  methods: {}
}
</script>
