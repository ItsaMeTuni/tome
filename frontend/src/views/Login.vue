<template>
  <v-app>
    <v-main app>
      <v-container
        class="fill-height"
        fluid
      >
        <v-row
          align="center"
          justify="center"
        >
          <v-col
            cols="12"
            sm="8"
            md="4"
          >
            <v-card>
              <v-toolbar flat color="primary">
                <v-toolbar-title>Login</v-toolbar-title>
                <v-progress-linear
                  :active="hasSubmitted"
                  :indeterminate="true"
                  absolute
                  bottom
                  color="secondary"
                ></v-progress-linear>
              </v-toolbar>
              <v-form v-model="valid" @submit.prevent="handleSubmit" lazy-validation>
                <v-card-text>
                  <v-alert type="error" v-model="showAlert" dismissible>
                    <span>{{ loginState }}</span>
                  </v-alert>
                  <v-text-field
                    label="Email"
                    name="email"
                    prepend-icon="mdi-email"
                    type="text"
                    required
                    :rules="[v => validate(v) || 'Enter a valid email address']"
                    v-model="email"
                  ></v-text-field>
                  <v-text-field
                    label="Password"
                    name="password"
                    prepend-icon="mdi-asterisk"
                    :type="passwordVisible ? 'text' : 'password'"
                    required
                    :rules="[v => !!v || 'This field is required']"
                    v-model="password"
                  >
                    <template v-slot:append>
                      <v-btn icon @click="passwordVisible = !passwordVisible">
                        <v-icon>
                          {{ passwordVisible ? 'mdi-eye-off' : 'mdi-eye' }}
                        </v-icon>
                      </v-btn>
                    </template>
                  </v-text-field>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="accent" :disabled="!valid" type="submit">Login</v-btn>
                </v-card-actions>
              </v-form>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
    <v-footer app>
      Tome {{ version }}
    </v-footer>
  </v-app>
</template>

<script>
import { validate } from 'email-validator'

export default {
  name: 'Login',
  methods: {
    handleSubmit () {
      this.hasSubmitted = true
      const { email, password } = this
      this.$store.dispatch('doLogin', { email, password })
    },
    validate
  },
  data: () => ({
    valid: false,
    hasSubmitted: false,
    email: '',
    password: '',
    showAlert: false,
    passwordVisible: false
  }),
  computed: {
    version () {
      return this.$store.state.version
    },
    loginState () {
      return this.$store.state.login.loginState
    }
  },
  watch: {
    loginState (value) {
      if (this.hasSubmitted) {
        this.hasSubmitted = false
        if (value === true) {
          this.$router.push('/')
        } else {
          this.showAlert = true
          this.password = ''
        }
      }
    },
    showAlert (value) {
      if (!value) {
        this.$store.commit('login.setLoginState', false)
      }
    }
  }
}
</script>

<style lang="scss"></style>
