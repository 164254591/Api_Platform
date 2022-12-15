<template>
  <div style="height: 100%">
      <el-container style="height: 100%">
        <el-aside width="200px">
          <Menu></Menu>
        </el-aside>
        <el-container>
          <el-header style="height: 80px;line-height: 80px">
            <h1>在线抓包导入  <span style="color: grey;font-size: xx-small">（手机挂上代理和端口，触发的请求都会导入到打开开关的项目中）</span> </h1>
          </el-header>
          <el-main>


            <el-card shadow="hover" style="width: 48%;float: left">
              <h1> 手机挂此代理：<span style="color: #42b983" v-text="get_host()"></span></h1>
            </el-card>
            <el-card shadow="hover" style="width: 48%;float:right;">
              <el-table :data="project_list_data">
                <el-table-column label-width="100%">
                  <template slot-scope="scope">
                    <el-button size="mini" type="success" @click="change_catch_status(scope.row.id)">开关</el-button>
                  </template>
                </el-table-column>
                <el-table-column label="当前可接收状态" label-width="100%">
                   <template slot-scope="scope">
                    <span :style="{color:get_color(scope.row.catch_status)}">{{scope.row.catch_status}}</span>
                  </template>
                </el-table-column>
                <el-table-column label="项目id" label-width="100%">
                   <template slot-scope="scope">
                    <span>{{scope.row.id}}</span>
                  </template>
                </el-table-column>
                <el-table-column label="项目名字" label-width="100%">
                   <template slot-scope="scope">
                    <span>{{scope.row.name}}</span>
                  </template>
                </el-table-column>


              </el-table>
            </el-card>


          </el-main>
        </el-container>
      </el-container>
  </div>
</template>

<script>
import Menu from "@/components/Menu";
import axios from "axios";
export default {
  name: "Api_catch",
  data() {
    return {
      file_name:'',
      project_list_data:[],
    }
  },
  methods: {
    get_host(){
      return process.env.VUE_APP_BASE_URL.split('://')[1].split(':')[0]+':8085'
    },
    get_color(result){
      if(result.toString()=='true'){
        return 'green'
      }else{
        return 'red'
      }
    },
    change_catch_status(id){
      axios.get('/change_catch_status/',{
        params:{
          project_id:id,
        }}).then(res=>{
          this.project_list_data=res.data

      })
    }


  },
  mounted() {
    axios.get('/get_project_list/').then(res=>{
      this.project_list_data=res.data
    })

  },
  components: {
    Menu,
    },

}
</script>

<style scoped>

</style>