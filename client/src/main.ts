import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import './tailwind.css';
import "./index.css";
import './assets/global.css';


const app = createApp(App);

app.use(store);
app.use(router);

// store.dispatch('checkAuth').then(() => {
app.mount('#app');
// });