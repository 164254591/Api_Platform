<template>
  <div style="height: 100%">
    <el-container style="height: 100%">
      <el-aside width="200px">
        <Menu></Menu>
      </el-aside>
      <el-main>
        <h1>权限管理 <span style="color: crimson;font-size: xx-small"> (此页面仅限超级管理员使用)</span></h1>
        <el-table
            :data="power_list_data"
            stripe
            style="max-width: 70%;min-height: 100%;overflow-y: auto;float: left">
          <el-table-column
              prop="id"
              label="ID"
              width="100">
          </el-table-column>
          <el-table-column
              prop="name"
              label="名称"
              width="150">
          </el-table-column>
          <el-table-column
              prop="path"
              label="监管路由"
              width="250">
          </el-table-column>
          <el-table-column
              prop="users"
              label="用户"
          >
          </el-table-column>
          <el-table-column>
            <template slot="header">
              <el-button type="primary" style="width: 151px" @click="add_power()">新增权限</el-button>
            </template>
            <template slot-scope="scope">
              <el-button size="mini" type="success" @click="edit_power(scope.$index)">编辑</el-button>
              <el-button size="mini" type="danger" @click="delete_power(scope.row.id)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-input
        type="textarea"
        :rows="30"
        v-model="all_paths"
        style="position: fixed;right: 20px;max-width: 26%;min-height: 100%;box-shadow: 4px 4px 10px gray">

        </el-input>
      </el-main>
    </el-container>

    <el-dialog title="编辑权限" :visible.sync="dialogFormVisible">
      <el-form :model="form_data" label-position="left">
        <el-form-item label="权限id:" label-width="80px">
          <el-input disabled="" v-model="form_data.id" autocomplete="off"></el-input>
        </el-form-item>

        <el-form-item label="权限名称:" label-width="80px">
          <el-input v-model="form_data.name" autocomplete="off"></el-input>
        </el-form-item>

        <el-form-item label="管控path:" label-width="80px">
          <el-input v-model="form_data.path" autocomplete="off"></el-input>
        </el-form-item>

        <el-form-item label="人员:" label-width="80px">
          <el-select v-model="form_data.users" multiple placeholder="请选择" style="width: 100%">
            <el-option
                v-for="i in all_user"
                :key="i.id"
                :label="i.id + '-' + i.username + '-' + i.title"
                :value="i.id + '-' + i.username + '-' + i.title+ ' ；' ">
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="save_power">保 存</el-button>
      </div>
    </el-dialog>


  </div>
</template>

<script>
import Menu from "@/components/Menu";
import axios from "axios";

export default {
  name: "Power_list",
  data() {
    return {
      dialogFormVisible: false,
      power_list_data: [],
      all_user:[],
      all_paths:'',
      form_data: {
        id: '',
        name: '',
        users: '',
        path: '',
      },
    }
  },
  methods: {
    edit_power(index) {
      this.form_data = this.power_list_data[index];
      this.dialogFormVisible = true;
    },
    add_power(index) {
      axios.get('http://localhost:8000/add_power/').then(res => {
        this.power_list_data = res.data.power_list_data
      })
    },
    delete_power(id) {
      axios.get('http://localhost:8000/delete_power/', {
        params: {
          id: id,
        }
      }).then(res => {
        this.power_list_data = res.data.power_list_data;
        this.$message({
          message: "删除成功！",
          type: "success",
        })
      })
    },
    save_power() {
      axios.post('http://localhost:8000/save_power/', this.form_data).then(res => {
        this.power_list_data = res.data.power_list_data;
        this.dialogFormVisible = false;
      })
    }

  },
  components: {
    Menu,
  },
  mounted() {
    axios.get('http://localhost:8000/get_power_list/').then(res => {
      this.power_list_data = res.data.power_list_data;
      this.all_user = res.data.all_user;
      this.all_paths = res.data.all_paths;
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