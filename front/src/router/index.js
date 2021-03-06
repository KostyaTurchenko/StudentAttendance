import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../store/index.js'

Vue.use(VueRouter)

const routes = [
    {
        path: '/authorization',
        name: 'Authorization',
        component: () => import('../components/Authorization.vue'),
        beforeEnter (to, from, next) {
            if (store.getters.isAuthenticated) {
                next('/')
            } else {
                next()
            }
        }
    },
    {
        path: '/attendance',
        name: 'Attendance',
        component: () => import('../components/Attendance.vue'),
        beforeEnter (to, from, next) {
            if (!store.getters.isAuthenticated) {
                next('/authorization')
            } else {
                next()
            }
        }
    },

  {
    path: '/',
    name: 'Home',
    component: () => import('../components/Home.vue')
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
