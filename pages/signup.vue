<template>
  <v-app>
    <v-container>
      <v-row>
        <v-col cols="12" md="4" center>
          <h1>Signup</h1>
          <v-form>
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
              v-model="username"
              :error-messages="usernameErrors"
              :counter="10"
              label="Username"
              prepend-icon="mdi-format-text"
              required
              @input="$v.username.$touch()"
              @blur="$v.username.$touch()"
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

            <v-file-input label="Attach profile picture"></v-file-input>

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

            <v-btn class="mr-4" color="primary" dark rounded @click="submit"
              >submit</v-btn
            >
            <v-btn color="primary" rounded @click="clear">clear</v-btn>
          </v-form>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>
<script>
import { validationMixin } from 'vuelidate'
import { required, maxLength, email, sameAs } from 'vuelidate/lib/validators'

export default {
  mixins: [validationMixin],

  validations: {
    name: { required, maxLength: maxLength(40) },
    username: { required, maxLength: maxLength(10) },
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
      username: '',
      email: '',
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
    usernameErrors() {
      const errors = []
      if (!this.$v.username.$dirty) return errors
      !this.$v.username.maxLength &&
        errors.push('Username must be at most 10 characters long')
      !this.$v.username.required && errors.push('Username is required.')
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
    submit() {
      this.$v.$touch()
    },
    clear() {
      this.$v.$reset()
      this.username = ''
      this.password = ''
      this.passwordConfirmation = ''
      this.name = ''
      this.email = ''
      this.checkbox = false
    }
  }
}
</script>
