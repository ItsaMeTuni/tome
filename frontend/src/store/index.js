import Vue from 'vue'
import Vuex from 'vuex'

import login from './login'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    version: require('@/../package.json').version
  },
  mutations: {
  },
  actions: {
    async apiRequest ({ state }, { method, path, data }) {
      return await fetch(path, {
        method,
        body: data === undefined ? data : JSON.stringify(data),
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + state.login.loginToken
        }
      })
    }
  },
  modules: {
    login
  }
})
