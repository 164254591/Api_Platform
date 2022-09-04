<template>
  <div class="home" style="height: 100%">
   <el-container style="height: 100%">
      <el-aside width="200px">
        <Menu></Menu>
      </el-aside>
      <el-container >
          <el-header style="height: 80px">

             <el-row :gutter="5" style="margin-top: 5px;">
              <el-col :span="6">
                <div class="staticbanner" style="background-color: #81c784;">
                  <div class="title" >
                   <p>官方接口数量：{{ real_time_datas.ApiShop_count }}</p>
                    <el-tag style="color: #81c784">实时</el-tag>
                  </div>
                </div>
              </el-col>

              <el-col :span="6">
                <div class="staticbanner" style="background-color: #f8b44f">
                  <div class="title">
                   <p>未读消息数量：{{real_time_datas.UnReadNews_count}}</p>
                    <el-tag style="color: #f8b44f">实时</el-tag>
                  </div>
                </div>
              </el-col>

              <el-col :span="6">
                <div class="staticbanner" style="background-color: #4cb5f6">
                  <div class="title">
                   <p>用例执行数量：{{real_time_datas.RunCase_count}}</p>
                    <el-tag style="color: #4cb5f6">实时</el-tag>
                  </div>
                </div>
              </el-col>

              <el-col :span="6">
                <div class="staticbanner" style="background-color: #f88277">
                  <div class="title">
                   <p>导入接口数量：{{real_time_datas.Import_count}}</p>
                    <el-tag style="color: #f88277">实时</el-tag>
                  </div>
                </div>
              </el-col>
             </el-row>
          </el-header>
          <el-main>
            <el-card class="box-card" style="overflow-y:auto;width: 30%;float: left;margin-right: 10px;">
                  <div slot="header" class="clearfix" >
                   <span>项目总览</span>
                  </div >
                  <p style="margin: 8px">项目总数：{{tj_datas.overview.project_count}}</p>
                  <p style="margin: 8px">接口总数：{{tj_datas.overview.api_count}}</p>
                  <p style="margin: 8px">用例总数：{{tj_datas.overview.case_count}}</p>
                  <p style="margin: 8px">用户总数：{{tj_datas.overview.user_count}}</p>
                  <p style="margin: 8px">环境总数：{{tj_datas.overview.env_count}}</p>

            </el-card>
            <el-card class="box-card" style="overflow-y:auto;width: -webkit-calc(70% - 20px)">
                  <div slot="header" class="clearfix">
                   <span>监控情况</span>
                  </div>
                    <span style="font-size: small">用例通过率</span>
                    <el-progress style="margin-bottom: 10px" :text-inside="true" :stroke-width="18" :percentage="tj_datas.monitors.case_pass"></el-progress>
                    <span style="font-size: small">接口通过率</span>
                    <el-progress style="margin-bottom: 10px" :text-inside="true" :stroke-width="18" :percentage="tj_datas.monitors.api_pass" status="success"></el-progress>
                    <span style="font-size: small">失败通过率</span>
                    <el-progress style="margin-bottom: 10px" :text-inside="true" :stroke-width="18" :percentage="tj_datas.monitors.case_fail" status="warning"></el-progress>
            </el-card>
            <el-card class="box-card" style="overflow-y:auto;width: -webkit-calc(60% - 20px);float: left;margin-right: 10px;">
                  <div slot="header" class="clearfix">
                   <span>个人贡献</span>
                  </div>
                    <table class="table">
                      <thead>
                      <tr>
                        <th>个人项目占比</th>
                        <th>个人用例占比</th>
                        <th>个人接口占比</th>
                        <th>贡献度占比</th>
                      </tr>
                      </thead>
                      <tbody>
                      <tr>
                        <td> <el-progress type="circle" :percentage="tj_datas.contributes.project" color="#42b983" ></el-progress></td>
                        <td> <el-progress type="circle" :percentage="tj_datas.contributes.case" color="#adc9ad"></el-progress></td>
                        <td> <el-progress type="circle" :percentage="tj_datas.contributes.api" color="antiquewhite"></el-progress></td>
                        <td><el-progress type="circle" :percentage="tj_datas.contributes.monitor" color="darkorange"></el-progress></td>
                      </tr>

                      </tbody>
                    </table>


            </el-card>
            <el-card class="box-card" style="width:40%;overflow-y: auto">
                      <div slot="header" class="clearfix">
                        <span>待处理消息</span>
                          <a href="#/send_news">
                              <el-button style="float: right; padding: 3px 0" type="text">进入详情</el-button>
                          </a>
                      </div>
                      <div v-for="o in tj_datas.news" :key="o" class="text item" >
                        {{ '来自' + o.from_user_name +'的未读消息： ' + o.content }}
                      </div>
                </el-card>
          </el-main>
          <el-footer style="height: 20%" >
                <el-card class="box-card" style="min-height: 85%;text-align: left;margin-top: 18px;line-height: 20px;margin-bottom: 18px;background-color: #d5e8d5;overflow-y: auto">
                  <div v-for="o in tj_datas.notices " :key="o" class="text item">
                    {{'平台更新日志 :' + o.content }}
                  </div>
                </el-card>
          </el-footer>
      </el-container>
   </el-container>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'
import Menu from '../components/Menu.vue'
import axios from 'axios'

export default {
  name: 'home',
  data(){
    return {
      tj_datas:{
        notices:[],
        news:[],
        overview:{
                  project_count:0,
                  api_count:0,
                  case_count:0,
                  user_count:0,
                  env_count:0
                },
        monitors:{
                  case_pass:0,
                  api_pass:0,
                  case_fail:0
                },
        contributes:{
                  project:0,
                  case:0,
                  api:0,
                  monitor:0
                },

      },
      real_time_datas:{
        ApiShop_count:0,
        UnReadNews_count:0,
        RunCase_count:0,
        Import_count:0
      },
    };
  },
  methods:{

  },
  components: {
    Menu,
  },
  // 进入页面先刷新请求数据
  mounted:function () {
    axios('http://localhost:8000/get_tj_datas/').then(res=>{
      this.tj_datas = res.data;
    });
     axios.get('http://localhost:8000/get_real_time_datas').then(res=>{
        this.real_time_datas = res.data;
    });

     // 刷新间隔，每1000毫秒刷新一次
    setInterval(()=>{
      axios.get('http://localhost:8000/get_real_time_datas').then(res=>{
        this.real_time_datas = res.data;
    }
      )},10000
    )
  }
}
</script>

<style>
  .el-header, .el-footer {
    background-color: #B3C0D1;
    color: #333;
    height: 80px;
  }

  .el-aside {
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    line-height: 200px;
  }

  .el-main {
    background-color: #E9EEF3;
    color: #333;
    text-align: left;
    line-height: 25px;
  }
  .el-card{
    overflow-y: auto;
    margin-bottom: 20px;
  }

  body > .el-container {
    margin-bottom: 40px;
  }

  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }

  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }
  .text {
    font-size: 14px;
  }

  .item {
    padding: 5px 0;
  }

  .box-card {
    max-height: 46%;
    min-height: 46%;
  }
  th,td {
    text-align: center;
    width: 28%;
  }
  .staticbanner{
    color: white;
    height: 70px;
    border-radius: 3px;
    padding: 0 8px;

  }
  .title{
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  p{
    font-size: 20px;
    font-weight: bold;
  }
</style>