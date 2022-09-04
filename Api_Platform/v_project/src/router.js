import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Project_list from "@/views/Project_list";
import Project_detail from "@/views/Project_detail";
import Env_list from "@/views/Env_list";
import Api_shop from "@/views/Api_shop";
import User_detail from "@/views/User_detail";
import Send_news from "@/views/Send_news";
import Send_notice from "@/views/Send_notice";
import Look_log from "@/views/Look_log";
import Power_list from "@/views/Power_list";

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/project_list',
      name: 'project_list',
      component: Project_list
    },
    {
      path: '/project_detail',
      name: 'Project_detail',
      component: Project_detail
    },
    {
      path: '/env_list',
      name: 'Env_list',
      component: Env_list
    },
    {
      path: '/api_shop',
      name: 'Api_shop',
      component: Api_shop
    },
    {
      path: '/user_detail',
      name: 'User_detail',
      component: User_detail
    },
    {
      path: '/send_news',
      name: 'Send_news',
      component: Send_news
    },
    {
      path: '/send_notice',
      name: 'Send_notice',
      component: Send_notice
    },
    {
      path: '/look_log',
      name: 'Look_log',
      component: Look_log
    },
    {
      path: '/power_list',
      name: 'Power_list',
      component: Power_list
    },
  ]
})
