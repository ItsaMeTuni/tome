<template>
  <v-app>
    <v-navigation-drawer app permanent>
      <v-list>
        <v-list-item class="mt-n2">
          <v-list-item-icon>
            <v-icon large>mdi-cog</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>
              <h1>Settings</h1>
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider></v-divider>
        <v-list-item v-for="(item, index) in items" :key="index" :to="item.to">
          <v-list-item-icon>
            <v-icon>mdi-{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <template v-slot:append>
        <v-divider></v-divider>
        <div class="ma-2">
          <v-btn icon to="/">
            <v-icon>mdi-arrow-left</v-icon>
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>
    <v-main app>
      <div class="ma-4">
        <router-view></router-view>
      </div>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'Settings',
  data: () => ({
    items: [
      {
        icon: 'account',
        title: 'Account',
        to: '/settings/account'
      },
      {
        icon: 'lock',
        title: '2FA',
        to: '/settings/2fa'
      },
      {
        icon: 'key',
        title: 'API keys',
        to: '/settings/apikeys'
      },
      {
        icon: 'eye',
        title: 'Display',
        to: '/settings/display'
      },
      {
        icon: 'exit-to-app',
        title: 'Log Out',
        to: '/logout'
      }
    ]
  }),
  computed: {
    gravatarUrl () {
      const hash = '205e460b479e2e5b48aec07710c08d50'
      return `https://www.gravatar.com/avatar/${hash}?d=mp&r=x&s=200`
    },
    name () {
      return 'Scott Morrison'
    }
  }
}
</script>

<style lang="scss"></style>
