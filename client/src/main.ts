import { createApp } from 'vue'
import App from './App.vue'
import './assets/global.css'
import './assets/index.css'
import './assets/tailwind.css'
import router from './router'
import store from './store'

const app = createApp(App)

store.dispatch('companyProfile/loadProfileFromStorage')
store.dispatch('companyFinancials/loadFinancialsFromStorage')

app.use(store)
app.use(router)
app.mount('#app')
