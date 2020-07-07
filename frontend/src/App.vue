<template>
  <router-view/>
</template>

<script>
export default {
  name: 'App',
  watch: {
    '$vuetify.theme.dark' (value) {
      localStorage.setItem('com.pxeger.tome.ui.dark', value.toString())
    }
  }
}
</script>
