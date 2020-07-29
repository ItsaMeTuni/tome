<template>
  <v-app>
    <v-main app>
      <v-dialog :value="!hasLoggedOut" max-width="max(40vw, 60vh)" modal>
        <v-card>
          <v-card-title>
            Logout
          </v-card-title>
          <v-card-text>
            Are you sure you want to logout?
          </v-card-text>
          <v-card-actions class="ps-6 pb-4 mt-n2">
            <v-spacer></v-spacer>
            <v-btn outlined color="warning" @click="doLogout">Logout</v-btn>
            <v-btn outlined color="info" to="/">Cancel</v-btn>
            <v-spacer></v-spacer>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-dialog :value="hasLoggedOut" max-width="max(40vw, 60vh)" modal>
        <v-card>
          <v-card-title>
            Successfully logged out
          </v-card-title>
          <v-card-actions class="ps-6 pb-4 mt-n2">
            <v-spacer></v-spacer>
            <v-btn outlined color="info" to="/login">Go to Login</v-btn>
            <v-spacer></v-spacer>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'Logout',
  data: () => ({
    hasLoggedOut: false
  }),
  methods: {
    doLogout () {
      this.$store.commit('login/unsetLoginState')
      this.hasLoggedOut = true
    }
  }
}
</script>

<style lang="scss"></style>
