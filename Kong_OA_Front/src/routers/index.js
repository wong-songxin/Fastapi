// import {createRouter, createWebHistory} from 'vue-router'
// import HomeView from "../views/HomeView.vue";
// import LoginView from "../views/LoginView.vue";
// import Index from "../views/admin/Index.vue";
// import UserInfo from '../views/admin/UserInfo.vue';

// import $cookie from "vue-cookies";

// import {reqAuth} from "../api/system.js";

// import {definedMenus} from '../store/menus.js'

// const router = createRouter({
//     history: createWebHistory(),
//     routes: [
//         {
//             path: '/',
//             name: 'Home',
//             component: HomeView,
//             children: [
//                 // 首页一直带，无论任何用户登录，都能看到首页
//                 {
//                     path: 'index',
//                     name: 'Index',
//                     component: Index
//                 },
//                 {
//                     path: 'user_info',
//                     name: 'UserInfo',
//                     component: UserInfo
//                 }
//                 // 下面的路由，要动态生成--》通过后台动态路由接口--》接口返回什么，再加进去什么，所以下面注释掉

//             ]
//         },
//         {
//             path: '/login',
//             component: LoginView
//         },
//     ]

// })

// /*
// 用户登录成功后--》点击任何一个菜单，都会触发router.beforeEach的执行
// 我们把 发送请求获取动态路径的代码，放在 路由守卫中
//     -什么情况获取：没有加载过的情况
//     -什么情况不获取：一旦加载过，不用每次都去获取，节省效率
//         -有个字段标志：是否加载过---》这个字段放在pinia


//  */

// function menuToRoute(menu) {
//     // 一个个把动态菜单，追加到router中
//     if (!menu.component) {// 没有与之对应的组件--》说明是根，最顶层的
//         return null
//     }
//     let route = {
//         name: menu.name,
//         path: menu.path,
//         meta: {
//             icon: menu.icon,
//             title: menu.title
//         },
//     }
//     route.component = () => import(/* @vite-ignore */'../views/' + menu.component + '.vue')
//     return route
// }

// async function reqMenusFunc() {
//     let $store = definedMenus()

//     let res = await reqAuth()

//     console.log('后端返回的菜单：', res.nav)

//     $store.setMenuList(res.nav)
//     $store.setPermList(res.authoritys)

//     let newRoutes = router.options.routes

//     res.nav.forEach(menu => {
//         menu.children.forEach(e => {
//             let route = menuToRoute(e)

//             console.log('生成的动态路由：', route)

//             if (route) {
//                 newRoutes[0].children.push(route)
//             }
//         })
//     })

//     console.log('准备添加的路由：', newRoutes)

//     newRoutes.forEach((route) => {
//         router.addRoute(route)
//     })

//     console.log(
//         '最终注册的路由：',
//         router.getRoutes()
//     )

//     console.log(
//         '/admin/dicts 是否存在：',
//         router.getRoutes().find(r => r.path === '/admin/dicts')
//     )

//     $store.changeRouteStatus(true)
// }


// // 路由守卫--》在进入到某个地址之前，先执行这个代码，判断用户是否有权限
// // 在这里面我们可以通过判断：cookie中，如果有token，说明是登录了，要访问那个页面，就能进哪个页面
// // 如果token为空，访问任何页面，都重定向到login
// // to:去哪个路由对象，from是从哪个路由对象过来，next是个函数，如果允许它跳转，直接执行next()

// // router.beforeEach((to, from, next) => {
// //     let token = $cookie.get('token')
// //     //1  拿到pinia的menu的对象,这个初始化，不能放在外面--》如果放外面---》如果放外面，在main.js中导入import router from "./routers";，代码就会执行，这时候，pinia还没初始化呢
// //     let $store = definedMenus()
// //     //2 有没有发送请求获取过动态路由,目前是false
// //     let hasRoute = $store.hasRoutes
// //     if (to.path == '/login') {// 访问登录页面，直接去
// //         next()
// //     } else if (!token) {
// //         // 重定向到login
// //         next({path: '/login'})
// //     } else if (token && !hasRoute) { //token有值：登录了，但是hasRoute是false，还没有加载过动态路由--》发送请求获取动态路由
// //         reqMenusFunc()
// //     }
// //     next()
// // })
// router.beforeEach(async (to, from) => {
//     const token = $cookie.get('token')
//     const $store = definedMenus()

//     if (to.path === '/login') {
//         return true
//     }

//     if (!token) {
//         return '/login'
//     }

//     if (! $store.hasRoutes) {
//         await reqMenusFunc()

//         // 动态路由添加完成后，重新匹配当前地址
//         return to.fullPath
//     }

//     return true
// })

// router.afterEach((to) => {
//     const store = definedMenus()

//     // 首页不重复添加
//     if (!to.name || to.name === 'Home') {
//         return
//     }

//     // 找当前路由对应的菜单
//     const menu = store.menuList
//         .flatMap(item => item.children || [])
//         .find(item => item.name === to.name)

//     if (menu) {
//         store.addTab({
//             name: menu.name,
//             title: menu.title
//         })
//     }
// })

// export default router





//fixed
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from "../views/HomeView.vue"
import LoginView from "../views/LoginView.vue"
import Index from "../views/admin/Index.vue"
import UserInfo from "../views/admin/UserInfo.vue"

import $cookie from "vue-cookies"
import { reqAuth } from "../api/system.js"
import { definedMenus } from '../store/menus.js'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'Home',
            component: HomeView,
            children: [
                {
                    path: 'index',
                    name: 'Index',
                    component: Index
                },
                {
                    path: 'user_info',
                    name: 'UserInfo',
                    component: UserInfo
                }
            ]
        },
        {
            path: '/login',
            component: LoginView
        },
    ]
})


function menuToRoute(menu) {
    if (!menu.component) {
        return null
    }

    const route = {
        name: menu.name,
        path: menu.path,
        meta: {
            icon: menu.icon,
            title: menu.title
        },
        component: () =>
            import(/* @vite-ignore */ '../views/' + menu.component + '.vue')
    }

    return route
}

// 临时替换
// async function reqMenusFunc() {
//     const store = definedMenus()

//     const res = await reqAuth()

//     store.setMenuList(res.nav)
//     store.setPermList(res.authoritys)

//     res.nav.forEach(menu => {
//         menu.children.forEach(item => {
//             const route = menuToRoute(item)

//             if (route) {
//                 router.addRoute('Home', route)
//             }
//         })
//     })

//     store.changeRouteStatus(true)
// }


async function reqMenusFunc() {
    const store = definedMenus()

    const res = await reqAuth()

    // ① 后端原始菜单
    console.log('========== 后端返回的菜单 ==========')
    console.log(res.nav)

    store.setMenuList(res.nav)
    store.setPermList(res.authoritys)

    // ② Pinia 中保存的菜单
    console.log('========== store.menuList ==========')
    console.log(store.menuList)

    res.nav.forEach(menu => {
        console.log('========== 一级菜单 ==========')
        console.log(menu.title, menu)

        menu.children.forEach(item => {
            console.log('========== 准备生成路由 ==========')
            console.log('父菜单：', menu.title)
            console.log('子菜单：', item.title)
            console.log('子菜单ID：', item.value)
            console.log('组件：', item.component)
            console.log('path：', item.path)

            const route = menuToRoute(item)

            console.log('生成的 route：', route)

            if (route) {
                router.addRoute('Home', route)

                console.log('已经添加路由：', route.name)
            }
        })
    })

    // ③ 查看最终路由
    console.log('========== 最终 router.getRoutes() ==========')
    console.log(router.getRoutes())

    store.changeRouteStatus(true)
}



router.beforeEach(async (to) => {
    const token = $cookie.get('token')

    if (to.path === '/login') {
        return true
    }

    if (!token) {
        return '/login'
    }

    return true
})


router.afterEach((to) => {
    const store = definedMenus()

    if (!to.name || to.name === 'Home') {
        return
    }

    const menu = store.menuList
        .flatMap(item => item.children || [])
        .find(item => item.name === to.name)

    if (menu) {
        store.addTab({
            name: menu.name,
            title: menu.title
        })
    }
})


export async function initRouter() {
    const token = $cookie.get('token')

    if (token) {
        await reqMenusFunc()
    }

    return router
}
export default router
