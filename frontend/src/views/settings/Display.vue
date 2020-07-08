<template>
  <div>
    <h1>Display Settings</h1>
    <v-switch v-model="$vuetify.theme.dark" label="Dark theme"></v-switch>
  </div>
</template>

<script>
export default {
  name: 'DisplaySettings',
  data: () => ({})
}
</script>

<style lang="scss"></style>
