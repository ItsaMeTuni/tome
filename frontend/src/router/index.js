import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import store from '../store'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import(/* webpackChunkName: "login" */ '../views/Login.vue'),
    beforeEnter: (whither, whence, next) => {
      // go back if they're already logged in
      if (store.state.login.loginState === true) next(false)
      else next()
    }
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})
export default router

router.beforeEach((whither, whence, next) => {
  if (store.state.login.loginState !== true && whither.name !== 'Login') {
    next({ name: 'Login' })
  } else next()
})
