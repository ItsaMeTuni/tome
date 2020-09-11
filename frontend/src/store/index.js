import Vue from 'vue'
import Vuex from 'vuex'

import login from './login'
import account from './account'
import apikeys from './apikeys'
import twoFactor from './twoFactor'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    version: require('@/../package.json').version
  },
  mutations: {
  },
  actions: {
    async apiRequest ({ state, commit }, { method, path, data }) {
      const response = await fetch(path, {
        method,
        body: data === undefined ? data : JSON.stringify(data),
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + state.login.loginToken
        }
      })
      if (response.status === 401) {
        // Clone response so that we can read the body of the response
        // without preventing the caller of the request from reading it
        // again
        const clone = response.clone()
        const json = await clone.json()

        if (json.error === 'invalid token') {
          commit('login/unsetLoginState')
        }
      }
      return response
    }
  },
  modules: {
    login,
    account,
    apikeys,
    twoFactor
  }
})
