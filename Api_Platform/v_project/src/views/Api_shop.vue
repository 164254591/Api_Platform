<template>
  <div style="height: 100%">
    <el-container style="height: 100%">
      <el-aside width="200px">
        <Menu></Menu>
      </el-aside>
      <el-main>
        <h1>接口商店 <span style="color: crimson;font-size: xx-small"> (此页面不要随意删除信息)</span></h1>
        <el-table
            :data="api_shop_list"
            stripe
            style="width: 100%;overflow-y: auto">
          <el-table-column
              prop="id"
              label="id"
              width="100">
          </el-table-column>
          <el-table-column
              prop="name"
              label="接口名称"
              width="150">
          </el-table-column>
          <el-table-column
              prop="host"
              label="域名"
              width="200">
          </el-table-column>
          <el-table-column
              prop="path"
              label="路径"
              width="250">
          </el-table-column>
          <el-table-column
              prop="method"
              label="请求方式"
              width="100">
          </el-table-column>
          <el-table-column
              prop="params"
              label="参数"
              width="200">
          </el-table-column>
          <el-table-column
              prop="payload"
              label="请求体参数"
              width="200">
          </el-table-column>
          <el-table-column
              prop="des"
              label="描述"
              width="150">
          </el-table-column>
          <el-table-column>
            <template slot="header">
              <el-button type="primary" style="width: 151px" @click="add_api_shop()">新增接口</el-button>
            </template>
            <template slot-scope="scope">
              <el-button size="mini" type="success" @click="edit_api_shop(scope.$index)">编辑</el-button>
              <el-button size="mini" type="primary" @click="open_project_list(scope.row.id)">下载</el-button>
              <el-button size="mini" type="danger" @click="Delete_api_shop(scope.row.id)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-main>
    </el-container>

    <el-dialog title="创建/保存接口" :visible.sync="dialogFormVisible">
      <el-form :model="form_data"  label-position="left">
        <el-form-item label="接口名称:"  label-width="80px">
          <el-input v-model="form_data.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="域名:"  label-width="80px">
          <el-input v-model="form_data.host" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="路径:"  label-width="80px">
          <el-input v-model="form_data.path" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="请求头:"  label-width="80px">
          <el-input v-model="form_data.headers" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="url入参:"  label-width="80px">
          <el-input v-model="form_data.params" autocomplete="off"></el-input>
        </el-form-item>

        <el-form-item label="请求体参数:"  label-width="80px">
          <el-input v-model="form_data.paylod" autocomplete="off"></el-input>
        </el-form-item>

        <el-form-item label="请求方式:"  label-width="80px" >
          <el-radio-group v-model="form_data.method">
            <el-radio label="get">get</el-radio>
            <el-radio label="post">post</el-radio>
            <el-radio label="delete">delete</el-radio>
            <el-radio label="put">put</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="描  述:"  label-width="50px">
          <el-input v-model="form_data.des" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="save_api_shop">保 存</el-button>
      </div>
    </el-dialog>

    <el-dialog title="选择任意项目接收该接口" :visible.sync="dialogFormVisible2">
      <el-table :data="project_list_data" style="width: 100%">
        <el-table-column style="width: 100%">
          <template slot-scope="scope">
            <el-button size="mini" type="primary">下载</el-button>
          </template>
        </el-table-column>
        <el-table-column label="项目id" label-width="100%">
          <template slot-scope="scope">
            <span>{{scope.row.id}} </span>
          </template>
        </el-table-column>
        <el-table-column label="项目名称" label-width="100%">
          <template slot-scope="scope">
            <span>{{scope.row.name}} </span>
          </template>
        </el-table-column>
        <el-table-column label="项目描述" label-width="100%">
          <template slot-scope="scope">
            <span>{{scope.row.desc}} </span>
          </template>
        </el-table-column>
      </el-table>

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
      dialogFormVisible2:false,
      project_list_data:[],
      api_shop_list: [],
      form_data: {
        name: '',
        host: '',
        path:'',
        method:'',
        params:'',
        paylod:'',
        headers:'',
        des: '',
      }
    }
  },
  methods: {
    add_api_shop(){
      this.dialogFormVisible=true;
      this.form_data={
                        name: '',
                        host: '',
                        path:'',
                        method:'',
                        params:'',
                        paylod:'',
                        headers:'',
                        des: '',
                      };
    },
    edit_api_shop(index){
      this.dialogFormVisible=true;
      this.form_data = this.api_shop_list[index]

    },

    save_api_shop() {
      this.dialogFormVisible=false;
      axios.post('http://localhost:8000/save_api_shop/',this.form_data).then(res => {
        this.api_shop_list = res.data
        this.$message({
              message:"创建成功！",
              type:'success'
           })
      })
    },
    Delete_api_shop(api_shop_id) {
      axios.get('http://localhost:8000/delete_api_shop/', {
        params: {
          api_shop_id: api_shop_id
        }
      }).then(res => {
        return this.api_shop_list = res.data
      })
    },
    open_project_list(){
      this.dialogFormVisible2=true;
      axios.get('http://localhost:8000/get_project_list/').then(res=>{
        return this.project_list_data=res.data
      })
    }

  },
  components: {
    Menu,
  },
  mounted() {
    axios.get('http://localhost:8000/get_api_shop_list/').then(res => {
      return this.api_shop_list = res.data
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