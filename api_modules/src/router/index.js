import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [{
  path: '/login',
  component: () => import('@/views/login/index'),
  hidden: true
},
{
  path: '/404',
  component: () => import('@/views/404'),
  hidden: true
},
// 流量监控
{
  path: '/',
  component: Layout,
  meta: {
    // title: '流量监控',
    icon: 'dashboard'
  },
  children: [{
    path: '',
    name: '流量监控',
    component: () => import('@/views/monitor/index'),
    meta: {
      title: '流量监控'
    }
  }]
},
// 大盘行情
{
  path: '/share',
  component: Layout,
  meta: {
    title: '股票策略',
    icon: 'stock'
  },
  children: [{
    path: '/share/index',
    name: '股票排行',
    component: () => import('@/views/share/index'),
    meta: {
      title: '股票排行',
      icon: 'rank'
    }
  }, {
    path: '/share/detail/:code?',
    name: '股票详情',
    props: true,
    component: () => import('@/views/share/detail'),
    meta: {
      title: '股票详情',
      icon: 'detail'
    }
  }, {
    path: '/share/industry',
    name: '行业板块',
    component: () => import('@/views/share/industry'),
    meta: {
      title: '行业板块',
      icon: 'classify'
    }
  }, {
    path: '/share/stg',
    name: '投资策略',
    component: () => import('@/views/share/stg'),
    meta: {
      title: '投资策略',
      icon: 'stg'
    }
  }]
},
// 基金行情
{
  path: '/fund',
  component: Layout,
  meta: {
    title: '基金策略',
    icon: 'nested'
  },
  children: [{
    path: '/fund/index',
    name: '基金排行',
    component: () => import('@/views/fund/index'),
    meta: {
      title: '基金排行',
      icon: 'rank'
    }
  }, {
    path: '/fund/detail',
    name: '基金详情',
    component: () => import('@/views/fund/detail'),
    meta: {
      title: '基金详情',
      icon: 'detail'
    }
  }, {
    path: '/fund/stg',
    name: '基金策略',
    component: () => import('@/views/fund/stg'),
    meta: {
      title: '基金策略',
      icon: 'stg'
    }
  }]
},
// 网格交易
{
  path: '/grid',
  component: Layout,
  meta: {
    title: '网格交易',
    icon: 'grid'
  },
  children: [{
    path: '/fund/trade',
    name: '基金模拟',
    component: () => import('@/views/fund/trade'),
    meta: {
      title: '基金模拟',
      icon: 'fund'
    }
  }, {
    path: '/share/trade',
    name: '股票模拟',
    component: () => import('@/views/share/trade'),
    meta: {
      title: '股票模拟',
      icon: 'share'
    }
  }]
},
// 素材管理
{
  path: '/material',
  component: Layout,
  redirect: '/material/upload',
  meta: {
    title: '素材管理',
    icon: 'plane'
  },
  children: [{
    path: 'check-template',
    name: 'check-template',
    component: () => import('@/views/material/check-template'),
    meta: {
      title: '查看模板'
    }
  },
  {
    path: 'logo',
    name: 'logo',
    component: () => import('@/views/material/check-logo'),
    meta: {
      title: '查看logo'
    }
  },
  {
    path: 'generate',
    name: 'generate',
    component: () => import('@/views/material/generate'),
    meta: {
      title: '生成素材'
    }
  },
  {
    path: 'check',
    name: 'check',
    component: () => import('@/views/material/check'),
    meta: {
      title: '查看素材'
    }
  }
  ]
},
// 404 page must be placed at the end !!!
{
  path: '*',
  redirect: '/404',
  hidden: true
}
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({
    y: 0
  }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
