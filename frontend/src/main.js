import Vue from 'vue'
import App from './App.vue'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import './main.css'
import {store} from "@/store";

Vue.config.productionTip = false
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)

window.onmessage = function (e) {
  if (e.origin === 'http://localhost:5000') {
    const json = JSON.parse(e.data);

    localStorage.setItem('token', json.token);
    location.reload();
  }
}

new Vue({
  store,
  render: h => h(App),
}).$mount('#app')
