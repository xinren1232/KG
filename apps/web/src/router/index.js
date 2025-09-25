import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      title: '首页'
    }
  },
  {
    path: '/extract',
    name: 'DocumentExtraction',
    component: () => import('../views/DocumentExtraction.vue'),
    meta: {
      title: '文档解析'
    }
  },
  {
    path: '/graph',
    name: 'GraphExplorer',
    component: () => import('../views/GraphExplorer.vue'),
    meta: {
      title: '知识图谱'
    }
  },
  {
    path: '/dictionary',
    name: 'DictionaryManagement',
    component: () => import('../views/DictionaryManagement.vue'),
    meta: {
      title: '词典管理'
    }
  },
  {
    path: '/governance',
    name: 'DataGovernance',
    component: () => import('../views/DataGovernance.vue'),
    meta: {
      title: '数据治理'
    }
  },


]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta && to.meta.title) {
    document.title = `${String(to.meta.title)} - 质量知识图谱助手`
  }
  next()
})

export default router
