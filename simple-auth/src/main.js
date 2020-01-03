import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import BootstrapVue from "bootstrap-vue";
import { store } from "./store";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
import "./assets/css/style.css";
import axios from 'axios';

Vue.use(BootstrapVue);
//axios.defaults.baseURL = process.env.API_ENDPOINT;
axios.defaults.baseURL = "http://localhost:5000";
// Use axios globally
Vue.prototype.axios = axios

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
