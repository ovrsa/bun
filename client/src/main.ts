import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import './tailwind.css';
import './index.css';
import './assets/global.css';

const app = createApp(App);

store.dispatch('companyProfile/loadProfileFromStorage');
store.dispatch('companyFinancials/loadFinancialsFromStorage');

app.use(store);
app.use(router);
app.mount('#app');
