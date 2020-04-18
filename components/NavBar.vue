<template>
  <div class="nav">
    <!--El atributo app es para que Vuetify automaticamente se encargue del escalado del elemento-->
    <v-app-bar app color="primary" dense dark collapse-on-scroll flat>
      <v-toolbar-title>TT 2019-B052</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn
        v-for="link in links"
        :key="`${link.label}-header-link`"
        text
        rounded
        :to="link.url"
      >
        {{ link.label }}
      </v-btn>
    </v-app-bar>
  </div>
</template>
<!--Recibimos todos los links de layout.vue-->
<script>
export default {
  props: {
    links: {
      type: Array,
      required: true
    }
  }
}
</script>

<style></style>
