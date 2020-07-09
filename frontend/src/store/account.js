export default {
  namespaced: true,
  state: {
    name: null,
    email: null
  },
  mutations: {
    setName (state, value) {
      state.name = value
    },
    setEmail (state, value) {
      state.email = value
    }
  },
  actions: {
    changeName ({ commit, dispatch, state }, value) {
      const previous = state.name
      commit('setName', value)
      dispatch('apiRequest', {
        method: 'PATCH',
        path: '/api/me/name',
        data: value
      }, { root: true }).then((r) => { if (!r.ok) throw new Error() }).catch(() => {
        commit('setName', previous)
      })
    },
    changeEmail ({ commit, dispatch, state }, value) {
      const previous = state.email
      commit('setEmail', value)
      dispatch('apiRequest', {
        method: 'PATCH',
        path: '/api/me/email',
        data: value
      }, { root: true }).then((r) => { if (!r.ok) throw new Error() }).catch(() => {
        commit('setEmail', previous)
      })
    }
  }
}
