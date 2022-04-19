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
      path: '/demo2',
      name: 'demo2',
      component: () => import('../views/DemoView2.vue')
    }
  ]
})

export default router
