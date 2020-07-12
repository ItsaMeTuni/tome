<template>
  <div>
    <v-alert
      type="error"
      v-for="(error, i) in $store.state.account.errors"
      :key="i"
      dismissible
      @input="$event || $store.commit('account/delError', i)"
    >{{ error }}</v-alert>
    <h1>Account Settings</h1>
    <section class="mt-4">
      <h2 class="mb-2">General</h2>
      <p>Change general settings about your account</p>
      <v-form
        lazy-validation
        @submit.prevent="$store.dispatch('account/changeName')"
        class="d-flex"
        v-model="nameFormValid"
      >
        <v-text-field
          label="Name"
          name="name"
          outlined
          type="text"
          required
          :rules="[v => !!v || 'This field is required']"
          v-model="name"
        ></v-text-field>
        <v-btn
          type="submit"
          outlined
          color="info"
          class="align-self-center ms-3 mt-n8"
          :disabled="!nameFormValid"
        >Save</v-btn>
      </v-form>
      <v-form
        lazy-validation
        @submit.prevent="$store.dispatch('account/changeEmail')"
        class="d-flex"
        v-model="emailFormValid"
      >
        <v-text-field
          label="Email address"
          name="email"
          outlined
          type="text"
          required
          :rules="[v => validateEmail(v) || 'Enter a valid email address']"
          v-model="email"
        ></v-text-field>
        <v-btn
          type="submit"
          outlined color="info"
          class="align-self-center ms-3 mt-n8"
          :disabled="!emailFormValid"
        >Save</v-btn>
      </v-form>
    </section>
    <section class="mb-8">
      <h2 class="mb-2">Password</h2>
      <p>If you wish to change your password, you must first enter your current password.
        Make sure to choose a secure one!</p>
      <v-form
        lazy-validation
        @submit.prevent="$store.dispatch('account/changePassword')"
        v-model="passwordFormValid"
      >
        <div class="d-flex flex-wrap mx-n2">
          <Password
            outlined
            label="Current password"
            class="mx-2"
            v-model="currentPassword"
          ></Password>
          <Password
            outlined
            label="New password"
            class="mx-2"
            v-model="newPassword"
          ></Password>
        </div>
        <v-btn type="submit" outlined color="info" :disabled="!passwordFormValid">Change Password</v-btn>
      </v-form>
    </section>
    <section class="my-8">
      <h2 class="mb-2">Danger Zone</h2>
      <p>If you wish to delete your account and all associated content, you can do so here.
        Please note that this action is <strong>completely irreversible!</strong></p>
      <v-btn color="error" outlined @click="handleDeleteAccount">Delete Account</v-btn>
    </section>
  </div>
</template>

<script>
import { validate } from 'email-validator'
import Password from '@/components/Password'
import Store from '@/store'

export default {
  name: 'AccountSettings',
  data: () => ({
    passwordFormValid: true,
    emailFormValid: true,
    nameFormValid: true
  }),
  methods: {
    validateEmail: validate,
    handleDeleteAccount () {
      if (confirm('Are you completely sure you want to delete your account? This action' +
        'is completely irreversible! All of your data will be permanently deleted!')) {
        console.log('Deleting account')
      }
    }
  },
  components: {
    Password
  },
  computed: {
    name: {
      get () {
        return this.$store.state.account.name
      },
      set (val) {
        this.$store.commit('account/setName', val)
      }
    },
    email: {
      get () {
        return this.$store.state.account.email
      },
      set (val) {
        this.$store.commit('account/setEmail', val)
      }
    },
    currentPassword: {
      get () {
        return this.$store.state.account.currentPassword
      },
      set (val) {
        this.$store.commit('account/setCurrentPassword', val)
      }
    },
    newPassword: {
      get () {
        return this.$store.state.account.newPassword
      },
      set (val) {
        this.$store.commit('account/setNewPassword', val)
      }
    }
  },
  beforeRouteEnter (whither, whence, next) {
    Store.dispatch('account/fetchAccountDetails').then(next)
  }
}
</script>

<style lang="scss"></style>
