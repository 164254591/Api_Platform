import Vue from 'vue'
import App from './App.vue'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import JsonViewer from 'vue-json-viewer'
import axios from "axios";
import JsonExcel from 'vue-json-excel'
Vue.component('downloadExcel', JsonExcel)
Vue.use(ElementUI)
Vue.config.productionTip = false
Vue.use(JsonViewer)
axios.defaults.baseURL= process.env.VUE_APP_BASE_URL;
new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
