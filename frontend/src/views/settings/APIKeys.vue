<template>
  <div>
    <h1>API keys</h1>
    <p>API keys allow you to easily access the Tome API for automation, auditing, or
    alternative clients, without needing to implement the complex login flow.
    <a href="https://github.com/pxeger/tome/blob/master/docs/apikeys.md">Learn more</a>
    </p>
    <v-list two-line>
      <v-list-item v-for="(item, i) in apikeys" :key="i">
        <v-list-item-content>
          <v-list-item-title>{{ item.key }}</v-list-item-title>
          <v-list-item-subtitle>{{ item.scope.join(' ') }}</v-list-item-subtitle>
        </v-list-item-content>
        <v-list-item-action>
          <v-btn icon>
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </v-list-item-action>
      </v-list-item>
    </v-list>
    <v-form @submit.prevent="alert(1)" class="my-4">
      <h2>Create API key</h2>
      <p>Select scopes to add to your API key. You can find a full explanation of each
      scope at the docs</p>
      <v-card>
        <div class="d-flex flex-wrap t-scopes-container mx-auto">
          <v-checkbox
            v-for="(scope, i) in scopes"
            :key="i"
            :label="scope"
            class="mx-2"
          ></v-checkbox>
        </div>
      </v-card>
      <v-btn type="submit" outlined color="info">Create</v-btn>
    </v-form>
  </div>
</template>

<script>
export default {
  name: 'APIKeys',
  data: () => ({
    apikeys: [
      {
        key: '123456',
        scope: ['account.read', 'account.write']
      },
      {
        key: '7890abc',
        scope: ['account.read', 'account.write']
      }
    ],
    scopes: [
      'account.read',
      'account.write.email',
      'account.write.name',
      'account.delete',
      'account.password'
    ]
  })
}
</script>

<style lang="scss">
.t-scopes-container {
  width: 100%;
  margin: auto;
  & > div {
    width: 15em;
    margin-left: auto;
    margin-right: auto;
  }
}
</style>
