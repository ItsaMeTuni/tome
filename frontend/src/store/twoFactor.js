export default {
  namespaced: true,
  state: {
    errors: [],
    status: 'unknown',
    secret: null,
    qrCodeURL: null,
    recovery: null
  },
  mutations: {
    addError (state, error) {
      state.errors.push(error)
    },
    delError (state, index) {
      state.errors.splice(index, 0)
    },
    setStatus (state, value) {
      state.status = value
    },
    setSecret (state, value) {
      state.secret = value
    },
    setQRCodeURL (state, value) {
      state.qrCodeURL = value
    },
    setRecovery (state, value) {
      state.recovery = value
    },
    setFinished (state, value) {
      state.finished = value
    }
  },
  actions: {
    beginSetup ({ commit, dispatch }) {
      dispatch('apiRequest', {
        method: 'POST',
        path: '/api/me/two_factor/begin_setup'
      }, { root: true }).then(r => {
        r.json().then(d => {
          if (!r.ok) {
            commit('addError', d.error)
          } else {
            commit('setSecret', d.secret)
            commit('setQRCodeURL', d.qr_code_url)
            commit('setStatus', 'setup_in_progress')
          }
        })
      }).catch(e => {
        console.error(e)
        commit('addError', 'An error occurred')
      })
    },
    cancelSetup ({ commit, dispatch }) {
      dispatch('apiRequest', {
        method: 'POST',
        path: '/api/me/two_factor/cancel_setup'
      }, { root: true }).then(r => {
        r.json().then(d => {
          if (!r.ok) {
            commit('addError', d.error)
          } else {
            commit('setSecret', null)
            commit('setQRCodeURL', null)
            commit('setStatus', 'disabled')
          }
        })
      }).catch(e => {
        console.error(e)
        commit('addError', 'An error occurred')
      })
    },
    confirmSetup ({ commit, dispatch, state }) {
      dispatch('apiRequest', {
        method: 'POST',
        path: '/api/me/two_factor/confirm_setup',
        data: state.code
      }, { root: true }).then(r => {
        r.json().then(d => {
          if (!r.ok) {
            commit('addError', d.error)
          } else {
            commit('setRecovery', d)
            commit('setQRCodeURL', null)
            commit('setSecret', null)
            commit('setStatus', 'setup_complete')
          }
        })
      }).catch(e => {
        console.error(e)
        commit('addError', 'An error occurred')
      })
    },
    disable ({ commit, dispatch }) {
      dispatch('apiRequest', {
        method: 'DELETE',
        path: '/api/me/two_factor'
      }, { root: true }).then(r => {
        r.json().then(d => {
          if (!r.ok) {
            commit('addError', d.error)
          } else {
            commit('setStatus', 'disabled')
          }
        })
      }).catch(e => {
        console.error(e)
        commit('addError', 'An error occurred')
      })
    },
    regenerateRecovery ({ commit, dispatch }) {
      dispatch('apiRequest', {
        method: 'POST',
        path: '/api/me/two_factor/regenerate_recovery'
      }, { root: true }).then(r => {
        r.json().then(d => {
          if (!r.ok) {
            commit('addError', d.error)
          } else {
            commit('setRecovery', d)
            commit('setStatus', 'setup_complete')
          }
        })
      }).catch(e => {
        console.error(e)
        commit('addError', 'An error occurred')
      })
    },
    init ({ commit, dispatch }) {
      dispatch('apiRequest', {
        method: 'GET',
        path: '/api/me/two_factor'
      }, { root: true }).then(r => {
        r.json().then(d => {
          if (!r.ok) {
            commit('addError', d.error)
          } else {
            commit('setRecovery', d.recovery)
            commit('setStatus', d.status)
          }
        })
      })
    }
  }
}
