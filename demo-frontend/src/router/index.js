import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/demo-old',
      name: 'demo-old',
      component: () => import('../views/DemoViewOld.vue')
    }
  ]
})

export default router
