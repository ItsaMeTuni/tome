export default {
  namespaced: true,
  state: {
    name: null,
    email: null,
    errors: [],
    currentPassword: '',
    newPassword: ''
  },
  mutations: {
    setName (state, value) {
      state.name = value
    },
    setEmail (state, value) {
      state.email = value
    },
    setCurrentPassword (state, value) {
      state.currentPassword = value
    },
    setNewPassword (state, value) {
      state.newPassword = value
    },
    addError (state, error) {
      state.errors.push(error)
    },
    delError (state, idx) {
      state.errors.splice(idx, 1)
    }
  },
  actions: {
    changeName ({ dispatch, state, commit }) {
      dispatch(
        'apiRequest',
        { method: 'PATCH', path: '/api/me/name', data: state.name },
        { root: true }
      ).then(r => {
        if (!r.ok) {
          r.json().then(d => {
            commit('addError', d.error)
          })
        }
      }).catch(e => {
        commit('addError', 'An error occurred')
        console.error(e)
      })
    },
    changeEmail ({ dispatch, state, commit }) {
      dispatch(
        'apiRequest',
        { method: 'PATCH', path: '/api/me/email', data: state.email },
        { root: true }
      ).then(r => {
        if (!r.ok) {
          r.json().then(d => {
            commit('addError', d.error)
          })
        }
      }).catch(e => {
        commit('addError', 'An error occurred')
        console.error(e)
      })
    },
    changePassword ({ dispatch, state, commit }) {
      const data = {
        new: state.newPassword,
        current: state.currentPassword
      }
      dispatch(
        'apiRequest',
        { method: 'POST', path: '/api/me/password', data: data },
        { root: true }
      ).then(r => {
        if (!r.ok) {
          r.json().then(d => {
            commit('addError', d.error)
          })
        } else {
          commit('setCurrentPassword', null)
          commit('setNewPassword', null)
        }
      }).catch(e => {
        commit('addError', 'An error occurred')
        console.error(e)
      })
    },
    fetchAccountDetails ({ dispatch, commit }) {
      dispatch(
        'apiRequest',
        { method: 'GET', path: '/api/me' },
        { root: true }
      ).then(r => {
        r.json().then(d => {
          if (!r.ok) commit('addError', d.error)
          else {
            commit('setEmail', d.email)
            commit('setName', d.name)
          }
        })
      }).catch(e => {
        commit('addError', 'An error occurred')
        console.error(e)
      })
    }
  }
}
