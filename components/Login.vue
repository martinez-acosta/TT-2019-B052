<template>
  <v-card width="400" class="mx-auto mt-5">
    <!--
        The v-card component is a versatile component that can be used for anything from a panel to a static image. The card component has numerous helper components to make markup as easy as possible. Components that have no listed options use Vue's functional component option for faster rendering and serve as markup sugar to make building easier.
        -->
    <v-card-title>
      <h1 class="display-1">Login</h1>
    </v-card-title>
    <v-card-text>
      <v-form @submit.prevent="login">
        <v-text-field
          v-model="email"
          label="email"
          prepend-icon="mdi-account-circle"
        />
        <v-text-field
          v-model="password"
          :type="showPassword ? 'text' : 'password'"
          label="Password"
          prepend-icon="mdi-lock"
          :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          @click:append="showPassword = !showPassword"
        />
        <v-alert v-show="error" type="error">
          {{ error }}
        </v-alert>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn color="primary" text rounded to="/register">Signup</v-btn>
          <v-spacer></v-spacer>
          <v-btn color="primary" type="submit" text rounded>Login</v-btn>
        </v-card-actions>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      showPassword: false,
      password: '',
      error: ''
    }
  },
  computed: {
    loginErrors() {
      const errors = this.error
      return errors
    }
  },
  methods: {
    login() {
      // Ejecutamos la vuex action login
      // Enviamos el usuario y la contraseña
      // Después los enviamos a la ruta protegida
      this.$nuxt.$loading.start()
      this.$store
        .dispatch('calls/login', {
          email: this.email,
          password: this.password
        })
        .then(() => {
          this.$router.push({ name: 'workspace' })
        })
        .catch((err) => {
          this.$nuxt.$loading.fail()
          this.$nuxt.$loading.finish()
          console.log(err.response)
          this.error = err.response.data.error
        })
    },
    clear() {
      this.password = ''
      this.error = ''
      this.email = ''
    }
  }
}
</script>
