<template>
  <v-card width="400" class="mx-auto mt-5">
    <v-card-title>
      <h1 class="display-1">Signup</h1>
    </v-card-title>
    <v-card-text>
      <v-form @submit.prevent="register">
        <v-text-field
          v-model="name"
          :error-messages="nameErrors"
          :counter="40"
          label="Name"
          prepend-icon="mdi-format-text"
          required
          @input="$v.name.$touch()"
          @blur="$v.name.$touch()"
        ></v-text-field>

        <v-text-field
          v-model="password"
          :rules="passwordRules"
          :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
          :type="show ? 'text' : 'password'"
          label="Password"
          prepend-icon="mdi-form-textbox-password"
          required
          @click:append="show = !show"
        />
        <v-text-field
          v-model="passwordConfirmation"
          :rules="passwordRules"
          :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
          :type="show ? 'text' : 'password'"
          label="Confirm password"
          required
          prepend-icon="mdi-form-textbox-password"
          @click:append="show = !show"
        />

        <v-text-field
          v-model="email"
          :error-messages="emailErrors"
          label="E-mail"
          type="email"
          required
          prepend-icon="mdi-email"
          @input="$v.email.$touch()"
          @blur="$v.email.$touch()"
        ></v-text-field>

        <v-checkbox
          v-model="checkbox"
          :error-messages="checkboxErrors"
          label="Do you agree?"
          required
          @change="$v.checkbox.$touch()"
          @blur="$v.checkbox.$touch()"
        ></v-checkbox>
        <v-alert v-show="error" type="error">
          {{ error }}
        </v-alert>

        <v-btn color="primary" type="submit" dark rounded>submit</v-btn>
        <v-btn color="primary" rounded @click="clear">clear</v-btn>
      </v-form>
    </v-card-text>
  </v-card>
</template>
<script>
import { validationMixin } from 'vuelidate'
import { required, maxLength, email, sameAs } from 'vuelidate/lib/validators'

export default {
  mixins: [validationMixin],

  validations: {
    name: { required, maxLength: maxLength(40) },
    password: { required },
    passwordConfirmation: {
      required,
      sameAsPassword: sameAs('password')
    },
    email: { required, email },
    checkbox: {
      checked(val) {
        return val
      }
    }
  },

  data() {
    return {
      name: '',
      email: '',
      error: '',
      checkbox: false,
      show: false,
      password: '',
      passwordConfirmation: '',
      passwordRules: [
        (password) => !!password || 'Password is required',
        (password) =>
          password.length >= 6 || 'Password must be at least 6 characters',
        (confirmation) =>
          confirmation === this.password || 'Passwords must match'
      ]
    }
  },

  computed: {
    checkboxErrors() {
      const errors = []
      if (!this.$v.checkbox.$dirty) return errors
      !this.$v.checkbox.checked && errors.push('You must agree to continue!')
      return errors
    },
    nameErrors() {
      const errors = []
      if (!this.$v.name.$dirty) return errors
      !this.$v.name.maxLength &&
        errors.push('Name must be at most 40 characters long')
      !this.$v.name.required && errors.push('Name is required.')
      return errors
    },
    emailErrors() {
      const errors = []
      if (!this.$v.email.$dirty) return errors
      !this.$v.email.email && errors.push('Must be valid e-mail')
      !this.$v.email.required && errors.push('E-mail is required')
      return errors
    }
  },

  methods: {
    register() {
      this.$nuxt.$loading.start()
      this.$store
        .dispatch('calls/register', {
          // Enviamos un objeto, denotado por {}, que contiene el nombre, username, email y password
          name: this.name,
          email: this.email,
          password: this.password
        })
        .then(() => {
          this.$router.push({ name: 'login' })
        })
        .catch((err) => {
          this.$nuxt.$loading.fail()
          this.$nuxt.$loading.finish()
          // console.log(err.response)
          this.error = err.response.data.error
        })
    },
    clear() {
      this.$v.$reset()
      this.password = ''
      this.passwordConfirmation = ''
      this.error = ''
      this.name = ''
      this.email = ''
      this.checkbox = false
    }
  }
}
</script>
