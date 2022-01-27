import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import router from './router'
import Vuex from 'vuex'
import store from './store/store.js'

Vue.config.productionTip = false
Vue.use(Vuex)

new Vue({
  render: h => h(App),
  router,
  store,
  vuetify
}).$mount('#app')
