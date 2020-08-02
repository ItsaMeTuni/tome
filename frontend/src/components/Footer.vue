<template>
  <v-footer app>
    <a href="https://github.com/pxeger/tome" class="not-link" target="_blank">
      Tome {{ version }}
    </a>
    <v-spacer></v-spacer>
    <slot>
      <v-btn @click="toggleTheme" icon small>
        <v-icon>{{ $vuetify.theme.dark ? 'mdi-brightness-7' : 'mdi-brightness-2' }}</v-icon>
      </v-btn>
    </slot>
  </v-footer>
</template>

<script>
export default {
  name: 'Footer',
  computed: {
    version () {
      return this.$store.state.version
    }
  },
  methods: {
    toggleTheme () {
      this.$vuetify.theme.dark = !this.$vuetify.theme.dark
    }
  }
}
</script>

<style lang="scss">
a.not-link {
  color: inherit !important;
  text-decoration: none;
}
</style>
