export default {
  state: {
    loginToken: null,
    loginState: false
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
    }
  },
  actions: {
    async doLogin ({ commit }, { email, password }) {
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
      if (response.ok) {
        commit('setLoginToken', await response.json())
      } else {
        const data = await response.json()
        commit('setLoginState', data.error)
      }
    },
    doLogout ({ commit }) {
      commit('unsetLoginState')
    }
  }
}
