<template>
  <el-menu
      :default-active="da"
      class="el-menu-vertical-demo"
      router
      :default-openeds="['1','2','3']">
    <el-menu-item index="/">首页Home</el-menu-item>
        <el-submenu index="1">
          <template slot="title">
            <i class="el-icon-s-grid"></i>
            <span>功能区</span>
          </template>
              <el-menu-item index="/project_list/">项目管理</el-menu-item>
              <el-menu-item index="/env_list/">环境管理</el-menu-item>
              <el-menu-item index="/api_shop/">接口商店</el-menu-item>
              <el-menu-item index="/monitor/">线上监控</el-menu-item>

          <el-menu-item-group title="接口导入">
              <el-menu-item index="/Api_doc/">接口文档</el-menu-item>
              <el-menu-item index="/Api_postman/">Postman</el-menu-item>
              <el-menu-item index="1-7">在线抓包</el-menu-item>
              <el-menu-item index="1-8">其他</el-menu-item>
          </el-menu-item-group>
        </el-submenu>

        <el-submenu index="2">
          <template slot="title">
            <i class="el-icon-user-solid"></i>
            <span>用户区</span>
          </template>

              <el-menu-item index="/user_detail/">个人资料</el-menu-item>
              <el-menu-item index="2-2">个人贡献</el-menu-item>
              <el-menu-item index="/send_news/">发送消息</el-menu-item>
              <a href="http://localhost:8000/help/" style="text-decoration:none">
                <el-menu-item>帮助</el-menu-item>
              </a>
              <a href="http://localhost:8000/logout/">
                <el-menu-item>退出</el-menu-item>
              </a>
        </el-submenu>


    <el-submenu index="3">
      <template slot="title">
        <i class="el-icon-s-tools"></i>
        <span>维护区</span>
      </template>

      <a href="http://localhost:8000/admin/">
        <el-menu-item>进入后台</el-menu-item>
      </a>
      <a href="http://localhost:8000/admin/auth/user/">
        <el-menu-item>用户管理</el-menu-item>
      </a>
      <el-menu-item index="/look_log/">查看日志</el-menu-item>
      <el-menu-item index="/send_notice/">发布公告</el-menu-item>
      <el-menu-item index="/power_list/">权限管理</el-menu-item>
    </el-submenu>

  </el-menu>
</template>

<script>
export default {
  name: "Menu",
  data() {
    return {
      // da:'/project_list/'
      da: window.location.hash.split('#')[1].split('?')[0] // 对url进行分割，先以#分割，再以？分割

  }
  },

}
</script>

<style scoped>
a {
  text-decoration: none;
}

</style>