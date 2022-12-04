<template>
  <div style="height: 100%">
      <el-container style="height: 100%">
        <el-aside width="200px">
          <Menu></Menu>
        </el-aside>
        <el-container>
          <el-header style="height: 80px;line-height: 80px">
            <h1>Postman批量导入  <span style="color: grey;font-size: xx-small">（先在postman导出文件，上传到平台，再点击对应项目的导入按钮即可）</span> </h1>
          </el-header>
          <el-main>
            <el-input v-model="ad_url" style="width: 50%;margin-left: 25%;margin-bottom: 10px" placeholder="在此处粘贴文档地址">
             <el-button  slot="append" @click="jx()">解析</el-button>
            </el-input>

            <el-card shadow="hover" style="width: 48%;float: left">
              <el-upload
                  class="upload-demo"
                  :action="get_action()"
                  :limit="1"
                  name="postman_file"
                  :on-success="save_postman_file_name"
              >
                <el-button @click="">上传文件</el-button>
              </el-upload>
            </el-card>
            <el-card shadow="hover" style="width: 48%;float:right;">
              <el-table :data="project_list_data">
                <el-table-column label-width="100%">
                  <template slot-scope="scope">
                    <el-button size="mini" type="success" @click="import_api_postman(scope.row.id)">导入到此项目</el-button>
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
  name: "Api_postman",
  data() {
    return {
      file_name:'',
      project_list_data:[],
    }
  },
  methods: {
    save_postman_file_name(res,file){
      this.file_name=file.raw.name
    },
    get_action(){
      return process.env.VUE_APP_BASE_URL+'/upload_postman_file/'
    },
    import_api_postman(project_id){
      axios.get('/import_api_postman/',{
        params:{
          project_id:project_id,
          filename:filename,
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