const loginToken = localStorage.getItem('com.pxeger.tome.auth_token')

export default {
  namespaced: true,
  state: {
    loginToken,
    loginState: !!loginToken,
    needsTwoFactorUpgrade: false,
    twoFactorCode: ''
  },
  mutations: {
    setLoginToken (state, token) {
      state.loginToken = token
      state.loginState = true
      try {
        localStorage.setItem('com.pxeger.tome.auth_token', token)
      } catch (e) {
        console.error(e)
        alert('Could not access Local Storage. Perhaps try a different browser?')
      }
    },
    setLoginState (state, value) {
      state.loginState = value
    },
    unsetLoginState (state) {
      state.loginState = false
      state.loginToken = null
      localStorage.removeItem('com.pxeger.tome.auth_token')
    },
    setNeedsTwoFactorUpgrade (state, value) {
      state.needsTwoFactorUpgrade = value
    },
    setTwoFactorCode (state, value) {
      state.twoFactorCode = value
    }
  },
  actions: {
    async doLogin ({ commit }, { email, password }) {
      // not using apiRequest action because we don't send credentials
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify({
          email, password
        }),
        headers: {
          'Content-Type': 'application/json'
        },
        cache: 'no-cache',
        credentials: 'omit'
      })
      const json = await response.json()
      if (response.ok) {
        commit('setLoginToken', json.token)
        commit('setNeedsTwoFactorUpgrade', json.needs_two_factor_upgrade)
      } else {
        commit('setLoginState', json.error)
      }
    },
    async doTwoFactorUpgrade ({ commit, dispatch, state }) {
      const response = await dispatch('apiRequest', {
        path: '/api/auth/two_factor_upgrade',
        method: 'POST',
        data: state.twoFactorCode
      }, { root: true })
      const json = await response.json()
      if (response.ok) {
        commit('setLoginToken', json)
      } else {
        commit('setLoginState', json.error)
      }
    },
    doLogout ({ commit }) {
      commit('unsetLoginState')
    },
    async doRefresh ({ commit, dispatch }) {
      const response = await dispatch('apiRequest', {
        method: 'POST',
        path: '/api/auth/refresh'
      })
      if (response.ok) {
        commit('setLoginToken', await response.json())
      } else {
        const data = await response.json()
        commit('setLoginState', data.error)
      }
    }
  }
}
