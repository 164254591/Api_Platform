<template>
  <div class="home" style="height: 100%">
    <el-container style="height: 100%">
      <el-aside width="200px">
        <Menu></Menu>
      </el-aside>
      <el-container>
        <el-header style="height: 80px;line-height: 80px">
          <el-input
              placeholder="请输入项目名称"
              prefix-icon="el-icon-search"
              style="width: 300px"
              v-model="keys"
              @change="change_search">
          </el-input>
        </el-header>
        <el-main>
            <el-table
              :data="project_list_data"
              stripe
              style="width: 100%;overflow-y: auto">
              <el-table-column
                prop="id"
                label="ID"
                width="180">
              </el-table-column>
              <el-table-column
                prop="name"
                label="项目名称"
                width="180">
              </el-table-column>
              <el-table-column
                prop="desc"
                label="项目描述">
              </el-table-column>
              <el-table-column
                prop="user_name"
                label="创建者">
              </el-table-column>

              <el-table-column >
                <template slot="header">
                  <el-button style="width: 121px" @click="Add_project"> 新增项目</el-button>
                </template>
                <template slot-scope="scope">
                    <router-link :to="'/project_detail?project_id='+scope.row.id">
                        <el-button size="mini" type="primary">进入</el-button>
                    </router-link>
                        <el-button size="mini" type="danger" @click="Delete_project(scope.row.id)">删除</el-button>
                </template>
              </el-table-column>

            </el-table>

        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import Menu from "@/components/Menu";
import axios from "axios";

export default {
  name: "Project_list",
  data() {
    return {
      keys: '',
      project_list_data: [],
    }
  },
  methods: {
    change_search() {
      axios.get('http://localhost:8000/get_project_list/',{
        params:{
          keys:this.keys
        }
      }).then(res=>{
        return this.project_list_data = res.data
      })

    },
    Delete_project(project_id){
      axios.get('http://localhost:8000/delete_project/',{
        params:{
          project_id:project_id
        }
      }).then(res => {
      return this.project_list_data = res.data})
    },
    Add_project(){
      axios.get('http://localhost:8000/add_project/').then(res=>{
        return this.project_list_data = res.data
      })
    }

  },
  mounted() {
    axios.get('http://localhost:8000/get_project_list/').then(res => {
      return this.project_list_data = res.data
    })
  },
  components: {
    Menu,
  },
}
</script>

<style scoped>
.el-header {
  background-color: #B3C0D1;
  color: #333;
  height: 80px;
}

.el-aside {
  background-color: #D3DCE6;
  color: #333;
  text-align: center;
  line-height: 200px;
   width:200px;
}

.el-main {
  background-color: #E9EEF3;
  color: #333;
  text-align: left;
  line-height: 25px;
}
</style>