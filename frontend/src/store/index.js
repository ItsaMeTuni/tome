import Vue from 'vue'
import Vuex from 'vuex'

import login from './login'
import account from './account'
import apikeys from './apikeys'

import router from '@/router'

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
      if (response.status === 401 && (await response.json()).error === 'invalid token') {
        commit('login/unsetLoginState')
        router.push('/login')
      }
      return response
    }
  },
  modules: {
    login,
    account,
    apikeys
  }
})
