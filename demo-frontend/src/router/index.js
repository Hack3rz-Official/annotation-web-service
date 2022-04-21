import { createRouter, createWebHistory } from 'vue-router'
import DemoView from '../views/DemoView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: DemoView
    },
    {
      path: '/demo-old',
      name: 'demo-old',
      component: () => import('../views/DemoViewOld.vue')
    }
  ]
})

export default router
