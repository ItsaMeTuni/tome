<template>
  <div>
    <v-alert
      type="error"
      v-for="(error, i) in $store.state.apikeys.errors"
      :key="i"
      dismissible
      @input="$event || $store.commit('account/delError', i)"
    >{{ error }}</v-alert>
    <h1>API keys</h1>
    <p>API keys allow you to easily access the Tome API for automation, auditing, or
    alternative clients, without needing to implement the complex login flow.
    <a href="https://github.com/pxeger/tome/blob/master/docs/apikeys.md">Learn more</a>
    </p>
    <v-list two-line v-if="apikeys.length">
      <v-list-item v-for="(item, i) in apikeys" :key="i">
        <v-list-item-content>
          <v-list-item-title>{{ item.id }}</v-list-item-title>
          <v-list-item-subtitle>{{ item.scope.join(' ') }}</v-list-item-subtitle>
        </v-list-item-content>
        <v-list-item-action>
          <v-btn icon @click="$store.dispatch('apikeys/deleteAPIKey', item.id)">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </v-list-item-action>
      </v-list-item>
    </v-list>
    <v-card v-else>
      <v-card-text>
        <div class="d-flex">
          <v-spacer></v-spacer>
          <p class="text-body-1">Nothing found.</p>
          <v-spacer></v-spacer>
        </div>
      </v-card-text>
    </v-card>
    <v-form @submit.prevent="handleSubmit" class="my-4">
      <h2>Create API key</h2>
      <p>Select scopes to add to your API key. You can find a full explanation of each
      scope at the docs</p>
      <v-card>
        <div class="d-flex flex-wrap t-scopes-container mx-auto">
          <v-checkbox
            v-for="(scope, i) in scopes"
            :key="i"
            :label="scope"
            v-model="selectedScope[scope]"
            class="mx-2"
          ></v-checkbox>
        </div>
      </v-card>
      <v-btn type="submit" outlined color="info">Create</v-btn>
    </v-form>
    <Password v-if="false"></Password>
  </div>
</template>

<script>
import Password from '@/components/Password'
import Store from '@/store'

export default {
  name: 'APIKeys',
  data: () => ({
    scopes: [
      // available scopes that api keys can use
      'account.read',
      'account.write.email',
      'account.write.name'
    ],
    selectedScope: {}
  }),
  computed: {
    apikeys () {
      return this.$store.state.apikeys.apikeys
    }
  },
  components: { Password },
  beforeRouteEnter (whither, whence, next) {
    console.log(Store)
    Store.dispatch('apikeys/fetchAPIKeys').then(next)
  },
  methods: {
    handleSubmit () {
      const scope = Object.keys(this.selectedScope).filter(k => this.selectedScope[k])
      this.$store.dispatch('apikeys/createAPIKey', scope)
      this.selectedScope = {}
    }
  }
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
