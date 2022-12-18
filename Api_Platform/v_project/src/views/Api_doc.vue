<template>
  <div style="height: 100%">
      <el-container style="height: 100%">
        <el-aside width="200px">
          <Menu></Menu>
        </el-aside>
        <el-container>
          <el-header style="height: 80px;line-height: 80px">
            <h1>接口文档导入  <span style="color: grey;font-size: xx-small">（先粘贴文档地址，然后点击解析按钮，再手动确认一遍后，点击对应项目的导入按钮即可）</span> </h1>
          </el-header>
          <el-main>
            <el-input v-model="ad_url" style="width: 50%;margin-left: 25%;margin-bottom: 10px" placeholder="在此处粘贴文档地址">
             <el-button  slot="append" @click="jx()">解析</el-button>
            </el-input>

            <el-card shadow="hover" style="width: 48%;float: left">
              <el-form :model="form_data">
                <el-form-item label="接口名称:" label-width="120px">
                  <el-input v-model="form_data.label" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="接口描述:" label-width="120px">
                  <el-input v-model="form_data.des" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="host域名:" label-width="120px">
                  <el-input v-model="form_data.host" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="path路径:" label-width="120px">
                  <el-input v-model="form_data.path" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="请求方式:" label-width="120px">
                  <el-radio-group v-model="form_data.method">
                    <el-radio label="get">get</el-radio>
                    <el-radio label="post">post</el-radio>
                    <el-radio label="delete">delete</el-radio>
                    <el-radio label="put">put</el-radio>
                  </el-radio-group>
                </el-form-item>
                <el-form-item label="请求头:" label-width="120px">
                  <el-input v-model="form_data.headers" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="Params:" label-width="120px">
                  <el-input v-model="form_data.params" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="payload_method:" label-width="120px">
                  <el-input v-model="form_data.payload_method" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="payload_fd:" label-width="120px">
                  <el-input v-model="form_data.payload_fd" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="payload_xwfu:" label-width="120px">
                  <el-input v-model="form_data.payload_xwfu" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="payload_raw_method:" label-width="150px">
                  <el-input v-model="form_data.payload_raw_method" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="payload_raw:" label-width="120px">
                  <el-input v-model="form_data.payload_raw" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="payload_GQL_q:" label-width="120px">
                  <el-input v-model="form_data.payload_GQL_q" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="payload_GQL_g:" label-width="120px">
                  <el-input v-model="form_data.payload_GQL_g" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="payload_binary:" label-width="120px">
                  <el-input v-model="form_data.payload_binary" autocomplete="off"></el-input>
                </el-form-item>

              </el-form>
            </el-card>
            <el-card shadow="hover" style="width: 48%;float:right;">
              <el-table :data="project_list_data">
                <el-table-column label-width="100%">
                  <template slot-scope="scope">
                    <el-button size="mini" type="success" @click="import_api_ad(scope.row.id)">导入到此项目</el-button>
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
  name: "Api_doc",
  data() {
    return {
      ad_url:'',
      form_data: {},
      project_list_data:[],


    }
  },
  methods: {
    jx(){
      axios.get('/jx_apiDoc/',{
        params:{
          ad_url:this.ad_url,
        }}).then(res=>{
        this.form_data = res.data
      })
    },
    import_api_ad(project_id){
      axios.post('/import_api_ad/',this.form_data,{
        params:{
          project_id:project_id,
        }}).then(res=>{
          this.$message({
            message:"导入成功！",
            type:"success"
          })
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