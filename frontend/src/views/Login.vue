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
                  :active="loading"
                  :indeterminate="true"
                  absolute
                  bottom
                  color="secondary"
                ></v-progress-linear>
              </v-toolbar>
              <!---->
              <v-form v-if="needsTwoFactorUpgrade" @submit.prevent="doTwoFactorUpgrade">
                <v-card-text>
                  <p>
                    Two-factor authentication is enabled on your account. Enter a code
                    generated by your app, or your recovery code, to complete login.
                  </p>
                  <v-alert type="error" v-model="showAlert" dismissible>
                    <span>{{ loginError }}</span>
                  </v-alert>
                  <v-text-field
                    v-model="twoFactorCode"
                    label="Code"
                    required
                  ></v-text-field>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="accent" type="submit">Ok</v-btn>
                </v-card-actions>
              </v-form>
              <!---->
              <v-form v-model="valid" @submit.prevent="doLogin" lazy-validation v-else>
                <v-card-text>
                  <v-alert type="error" v-model="showAlert" dismissible>
                    <span>{{ loginError }}</span>
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
                  <Password v-model="password" prepend></Password>
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
    <Footer></Footer>
  </v-app>
</template>

<script>
import { validate } from 'email-validator'
import Footer from '@/components/Footer'
import Password from '@/components/Password'
import { mapState } from 'vuex'

export default {
  name: 'Login',
  methods: {
    validate,
    async doLogin () {
      this.loading = true
      // not using apiRequest action because we don't send credentials
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify({
          email: this.email,
          password: this.password
        }),
        headers: {
          'Content-Type': 'application/json'
        },
        cache: 'no-cache',
        credentials: 'omit'
      })
      const json = await response.json()
      this.loading = false
      if (response.ok) {
        this.$store.commit('login/setLoginToken', {
          needsTwoFactorUpgrade: json.needs_two_factor_upgrade,
          token: json.token
        })
        if (!json.needs_two_factor_upgrade) this.$router.push('Home')
      } else {
        this.showAlert = true
        this.loginError = json.error
      }
    },
    async doTwoFactorUpgrade () {
      this.loading = true
      const response = await this.$store.dispatch('apiRequest', {
        path: '/api/auth/two_factor_upgrade',
        method: 'POST',
        data: this.twoFactorCode
      }, { root: true })
      const json = await response.json()
      this.loading = false
      if (response.ok) {
        this.$store.commit('login/setLoginToken', {
          needsTwoFactorUpgrade: false,
          token: json
        })
        this.$router.push('Home')
      } else {
        this.showAlert = true
        this.loginError = json.error
      }
    }
  },
  data: () => ({
    valid: false,
    loading: false,
    email: '',
    password: '',
    showAlert: false,
    passwordVisible: false,
    loginError: null,
    twoFactorCode: ''
  }),
  components: {
    Footer,
    Password
  },
  computed: mapState('login', ['needsTwoFactorUpgrade'])
}
</script>

<style lang="scss"></style>
