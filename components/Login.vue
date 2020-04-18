<template>
  <v-card width="400" class="mx-auto mt-5">
    <!--
        The v-card component is a versatile component that can be used for anything from a panel to a static image. The card component has numerous helper components to make markup as easy as possible. Components that have no listed options use Vue's functional component option for faster rendering and serve as markup sugar to make building easier.
        -->
    <v-card-title>
      <h1 class="display-1">Login</h1>
    </v-card-title>
    <v-card-text>
      <v-form>
        <v-text-field label="Username" prepend-icon="mdi-account-circle" />
        <v-text-field
          :type="showPassword ? 'text' : 'password'"
          label="Password"
          prepend-icon="mdi-lock"
          :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          @click:append="showPassword = !showPassword"
        />
      </v-form>
    </v-card-text>
    <v-divider></v-divider>
    <v-card-actions>
      <v-btn color="primary" text rounded to="/signup">Signup</v-btn>
      <v-spacer></v-spacer>
      <v-btn color="primary" text rounded>Login</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      showPassword: false
    }
  }
}
</script>
