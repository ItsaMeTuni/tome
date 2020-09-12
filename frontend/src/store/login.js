const LOCAL_STORAGE_TWO_FACTOR_NEEDED_KEY = 'com.pxeger.tome.needs_two_factor_upgrade'
const LOCAL_STORAGE_TOKEN_KEY = 'com.pxeger.tome.auth_token'
const needsTwoFactorUpgrade = !!localStorage.getItem(LOCAL_STORAGE_TWO_FACTOR_NEEDED_KEY)
const loginToken = localStorage.getItem(LOCAL_STORAGE_TOKEN_KEY)

export default {
  namespaced: true,
  state: {
    loginToken,
    needsTwoFactorUpgrade
  },
  getters: {
    isLoggedIn (state) {
      return state.loginToken && !state.needsTwoFactorUpgrade
    }
  },
  mutations: {
    setLoginToken (state, { needsTwoFactorUpgrade, token }) {
      state.loginToken = token
      state.needsTwoFactorUpgrade = needsTwoFactorUpgrade
      try {
        localStorage.setItem(LOCAL_STORAGE_TOKEN_KEY, token)
        localStorage.setItem(LOCAL_STORAGE_TWO_FACTOR_NEEDED_KEY, needsTwoFactorUpgrade)
      } catch (e) {
        console.error(e)
        alert('Could not access Local Storage. Perhaps try a different browser?')
      }
    },
    unsetLoginToken (state) {
      state.loginToken = null
      try {
        localStorage.removeItem(LOCAL_STORAGE_TOKEN_KEY)
        localStorage.removeItem(LOCAL_STORAGE_TWO_FACTOR_NEEDED_KEY)
      } catch (e) {
        console.error(e)
        alert('Could not access Local Storage. Perhaps try a different browser?')
      }
    }
  },
  actions: {
    async doRefresh ({ commit, dispatch, getters }) {
      if (getters.isLoggedIn) {
        const response = await dispatch('apiRequest', {
          method: 'POST',
          path: '/api/auth/refresh'
        }, { root: true })
        if (!response) return
        if (response.ok) {
          commit('setLoginToken', await response.json())
        } else {
          console.error(await response.json())
        }
      }
    }
  }
}
