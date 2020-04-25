<template>
  <div class="home">
    <h1>Welcome to the App!</h1>
    <!--<div v-if="!loggedIn">-->
    <div>
      To use this app you'll need to
      <nuxt-link to="/login">
        Login
      </nuxt-link>
      or
      <nuxt-link to="/register">
        Register
      </nuxt-link>
    </div>
  </div>
</template>

<script>
export default {
  components: {},
  head() {
    /* head() es para añadir el título de cada página al layout default.vue que recibe un string (el título de la página que está renderizando + la cadena "TT 2019-B052 por defecto" */
    /* hid,name y content son elementos para usarse con las SEO tags (gestores de búsqueda) y en cada página que creamos podemos sobreescribir las opciones que tiene por defecto el layout.vue */
    return {
      title: 'home',
      meta: [
        {
          hid: 'description',
          name: 'description',
          content:
            'Where you can find all the events taking place in your neighborhood'
        }
      ]
    }
  }
}
</script>

<style></style>
