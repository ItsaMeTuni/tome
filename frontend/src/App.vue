<template>
  <router-view/>
</template>

<script>
import Store from '@/store'

export default {
  name: 'App',
  watch: {
    '$vuetify.theme.dark' (value) {
      localStorage.setItem('com.pxeger.tome.ui.dark', value.toString())
    }
  },
  mounted () {
    Store.dispatch('login/doRefresh')
    // refresh login token every 5 minutes
    window.setInterval(() => Store.dispatch('login/doRefresh'), 300000)
  }
}
</script>
