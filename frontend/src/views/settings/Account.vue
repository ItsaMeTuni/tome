<template>
  <div>
    <h1>Account Settings</h1>
    <section class="mb-8 mt-4">
      <h2 class="mb-2">General</h2>
      <p>Change general settings about your account</p>
      <v-form lazy-validation @submit.prevent="handleGeneralSubmit">
        <v-text-field
          label="Name"
          name="name"
          outlined
          type="text"
          required
          :rules="[v => !!v || 'This field is required']"
          v-model="name"
        >{{ name }}</v-text-field>
        <v-text-field
          label="Email address"
          name="email"
          outlined
          type="text"
          required
          :rules="[v => validateEmail(v) || 'Enter a valid email address']"
          v-model="email"
        ></v-text-field>
        <v-btn type="submit" outlined color="info">Save</v-btn>
      </v-form>
    </section>
    <section class="my-8">
      <h2 class="mb-2">Password</h2>
      <p>If you wish to change your password, you must first enter your current password.
        Make sure to choose a secure one!</p>
      <v-form lazy-validation @submit.prevent="handlePasswordSubmit">
        <Password outlined label="Current Password"></Password>
        <Password outlined label="New Password"></Password>
        <v-btn type="submit" outlined color="info">Change Password</v-btn>
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

export default {
  name: 'AccountSettings',
  data: () => ({
    name: 'Scott Morrison',
    email: 'scott@gov.au'
  }),
  methods: {
    validateEmail: validate,
    handleGeneralSubmit () {
      alert(1)
    },
    handleDeleteAccount () {
      if (confirm('Are you completely sure you want to delete your account? This action' +
        'is completely irreversible! All of your data will be permanently deleted!')) {
        console.log('Deleting account')
      }
    },
    handlePasswordSubmit () {
      alert(1)
    }
  },
  components: {
    Password
  }
}
</script>

<style lang="scss"></style>
