<template>
  <div style="height: 100%">
    <el-container style="height: 100%">
      <el-aside width="200px">
        <Menu></Menu>
      </el-aside>
      <el-main>
        <h1>环境管理 <span style="color: crimson;font-size: xx-small"> (此页面不要随意删除信息)</span></h1>
        <el-table
            :data="env_list_data"
            stripe
            style="width: 100%;overflow-y: auto">
          <el-table-column
              prop="id"
              label="id"
              width="180">
          </el-table-column>
          <el-table-column
              prop="host"
              label="域名"
              width="280">
          </el-table-column>
          <el-table-column
              prop="type"
              label="类型"
              width="280">
            <template slot-scope="scope">
              <el-tag type="success">{{ scope.row.type }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column
              prop="des"
              label="描述"
              width="280">
          </el-table-column>
          <el-table-column>
            <template slot="header">
              <el-button type="primary" style="width: 121px" @click="dialogFormVisible=true">新增环境</el-button>
            </template>
            <template slot-scope="scope">
              <el-button size="mini" type="danger" @click="Delete_env(scope.row.id)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-main>
    </el-container>

    <el-dialog title="新增环境信息" :visible.sync="dialogFormVisible">
      <el-form :model="form_data"  label-position="left">
        <el-form-item label="环境域名:"  label-width="80px">
          <el-input v-model="form_data.host" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="类  型:"  label-width="80px" >
          <el-select v-model="form_data.type" placeholder="请选择环境标签" style="width: 100%">
            <el-option label="dev" value="开发环境"></el-option>
            <el-option label="SIT" value="测试环境"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="描  述:"  label-width="80px">
          <el-input v-model="form_data.des" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="Add_env">创 建</el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>
import Menu from "@/components/Menu";
import axios from "axios";

export default {
  name: "Env_list",
  data() {
    return {
      dialogFormVisible: false,
      env_list_data: [],
      form_data: {
        host: 'http://',
        type: '',
        des: '',
      }
    }
  },
  methods: {

    Add_env() {
      this.dialogFormVisible=false;
      axios.post('http://localhost:8000/add_env/',this.form_data).then(res => {
        this.env_list_data = res.data
        this.$message({
              message:"创建成功！",
              type:'success'
           })
      })
    },
    Delete_env(env_id) {
      axios.get('http://localhost:8000/delete_env/', {
        params: {
          env_id: env_id
        }
      }).then(res => {
        return this.env_list_data = res.data
      })
    },

  },
  components: {
    Menu,
  },
  mounted() {
    axios.get('http://localhost:8000/get_env_list/').then(res => {
      return this.env_list_data = res.data
    })
  },

}
</script>

<style scoped>
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
</style>