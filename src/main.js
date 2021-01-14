import Vue from 'vue'
import App from './App.vue'
import router from '@/router'
import Buefy from 'buefy'
import 'buefy/dist/buefy.css'
import '@fortawesome/fontawesome-free/css/all.css'

Vue.config.productionTip = false

Vue.use(Buefy, {
    defaultIconPack: 'fas',
    defaultContainerElement: '#content',
});

new Vue({
  render: h => h(App),
  router,
}).$mount('#app')
