import { createApp } from 'vue'
import './assets/css/gloabl.css'
import App from './App.vue'
import router, { initRouter } from "./routers"

import { createPinia } from 'pinia'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const app = createApp(App)

const pinia = createPinia()

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

app.use(pinia)
app.use(ElementPlus)

await initRouter()

app.use(router)

app.mount('#app')