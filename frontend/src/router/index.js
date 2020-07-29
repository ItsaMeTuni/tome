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
    component: () => import(/* webpackChunkName: "settings" */ '../views/Settings.vue'),
    children: [
      {
        path: 'account',
        name: 'Account',
        component: () => import(/* webpackChunkName: "settings-account" */ '../views/settings/Account.vue')
      },
      {
        path: '2fa',
        name: 'Two-factor authentication',
        component: () => import(/* webpackChunkName: "settings-two-factor" */ '../views/settings/TwoFactor.vue')
      },
      {
        path: 'display',
        name: 'Display',
        component: () => import(/* webpackChunkName: "settings-display" */ '../views/settings/Display.vue')
      },
      {
        path: 'apikeys',
        name: 'API keys',
        component: () => import(/* webpackChunkName: "settings-apikeys" */ '../views/settings/APIKeys.vue')
      }
    ]
  },
  {
    path: '/logout',
    name: 'Logout',
    component: () => import(/* webpackChunkName: "logout" */ '../views/Logout.vue')
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
