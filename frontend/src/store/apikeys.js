export default {
  namespaced: true,
  state: {
    errors: [],
    apikeys: []
  },
  mutations: {
    addError (state, error) {
      state.errors.push(error)
    },
    delError (state, idx) {
      state.errors.splice(idx, 1)
    },
    addAPIKey (state, value) {
      state.apikeys.push(value)
    },
    delAPIKey (state, id) {
      state.apikeys = state.apikeys.filter(k => k.id !== id)
    }
  },
  actions: {
    // TODO(pxeger) needs more DRY
    createAPIKey ({ commit, dispatch }, scope) {
      const payload = {
        duration: null,
        scope
      }
      const requestOptions = {
        method: 'POST',
        path: '/api/account/api_key',
        data: payload
      }
      dispatch('apiRequest', requestOptions, { root: true }).then(r => {
        r.json().then(d => {
          console.log(d)
          if (!r.ok) commit('addError', d.error)
          else {
            commit('addAPIKey', { id: d, ...payload })
          }
        })
      }).catch(e => {
        commit('addError', 'An error occurred')
        console.error(e)
      })
    },
    fetchAPIKeys ({ commit, dispatch }) {
      const requestOptions = {
        method: 'GET',
        path: '/api/account/api_key'
      }
      dispatch('apiRequest', requestOptions, { root: true }).then(r => {
        r.json().then(d => {
          if (!r.ok) commit('addError', d.error)
          else {
            for (const key of d) {
              key.scope = JSON.parse(key.scope)
              commit('addAPIKey', key)
            }
          }
        })
      }).catch(e => {
        commit('addError', 'An error occurred')
        console.error(e)
      })
    },
    deleteAPIKey ({ commit, dispatch }, id) {
      const requestOptions = {
        method: 'DELETE',
        path: '/api/account/api_key?id=' + id
      }
      dispatch('apiRequest', requestOptions, { root: true }).then(r => {
        r.json().then(d => {
          if (!r.ok) commit('addError', d.error)
          else commit('delAPIKey', id)
        })
      }).catch(e => {
        commit('addError', 'An error occurred')
        console.error(e)
      })
    }
  }
}
