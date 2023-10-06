import Vue from 'vue'
import VueRouter from 'vue-router'
import LogIn from '../views/LogIn.vue';
import EditTracker from '../views/EditTracker.vue';
import editUser from '../views/editUser.vue';
import logForm from '../views/LogForm.vue';
import DashBoard from '../views/DashBoard.vue';
import moreInfo from '../views/moreInfo.vue';
Vue.use(VueRouter)

const routes = [
  {path:'/',redirect:"/login"},
  { path: '/login', name:"Login",component: LogIn },
  { path: '/:user/Edit', name:"EditUser",component: editUser},
  { path: '/:user/newTracker',name:"newTracker", component: EditTracker },
  { path: '/:user/:ID/editTracker',name:"editTracker" ,component: EditTracker },
  { path: '/Log/:user/:ID', name:"newLog",component: logForm,props:{toEdit:false}},
  { path: '/EditLog/:user/:ID/:Entry',name:"editLog", component: logForm, props:{toEdit:true}},
  { path: '/Dashboard/:user', name:"dashboard",component: DashBoard },
  { path: '/view/:user/:ID', name:"moreInfo",component: moreInfo },
]

const router = new VueRouter({
  routes
})

export default router
