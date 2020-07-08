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
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import(/* webpackChunkName: "account" */ '../views/Settings.vue'),
    children: [
      {
        path: 'account',
        name: 'Account',
        component: () => import(/* webpackChunkName: "account" */ '../views/settings/Account.vue')
      },
      {
        path: 'display',
        name: 'Display',
        component: () => import(/* webpackChunkName: "account" */ '../views/settings/Display.vue')
      }
    ]
  },
  {
    path: '/logout',
    name: 'Logout',
    component: () => import(/* webpackChunkName: "login" */ '../views/Logout.vue')
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
