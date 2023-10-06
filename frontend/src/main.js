import Vue from 'vue'
import App from './App.vue'

Vue.config.productionTip = false
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import router from './router'
import VueCookies from 'vue-cookies'
import './registerServiceWorker'

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
Vue.use(VueCookies)
new Vue({
  el: '#app',
  router,
  render: h => h(App)
}).$mount('#app')
