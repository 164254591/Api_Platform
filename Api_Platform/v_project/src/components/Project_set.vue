<template>
<div>
  <h1>我是项目设置页</h1>
  <el-form :label-position="'left'" ref="form_data" :model="form_data"  label-width="80px">
      <el-form-item label="项目名称">
        <el-input v-model="form_data.name"></el-input>
      </el-form-item>

      <el-form-item label="项目描述">
        <el-input v-model="form_data.desc"></el-input>
      </el-form-item>


      <el-form-item label="mock方式">
        <el-radio-group v-model="form_data.mock">
          <el-radio label="mock_data">写死返回值</el-radio>
          <el-radio label="redirect">重定向到其他接口</el-radio>
        </el-radio-group>
      </el-form-item>

     <el-form-item label="私密项目">
        <el-switch v-model="form_data.priviate"></el-switch>
      </el-form-item>

     <el-form-item label="编辑权限">
        <el-checkbox-group v-model="form_data.power">
          <el-checkbox label="自己" name="power"></el-checkbox>
          <el-checkbox label="领导" name="power"></el-checkbox>
          <el-checkbox label="同事" name="power"></el-checkbox>
          <el-checkbox label="所有人" name="power"></el-checkbox>
        </el-checkbox-group>
     </el-form-item>

      <el-form-item label="业务线">
        <el-select v-model="form_data.bus_type" placeholder="请选择活动区域">
          <el-option label="APP线" value="app"></el-option>
          <el-option label="WEB线" value="web"></el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="公共变量">
        <el-input type="textarea" :rows="3" v-model="form_data.P_data" ></el-input>
      </el-form-item>


      <el-form-item label="登录变量">
        <el-input type="textarea" :rows="3" v-model="form_data.L_data" ></el-input>
      </el-form-item>

      <el-form-item label="加密算法">
        <el-input type="textarea" :rows="3" v-model="form_data.sign" ></el-input>
      </el-form-item>


      <el-form-item>
        <el-button type="primary" @click="Save_project">提交</el-button>
        <el-button>取消</el-button>
    </el-form-item>
  </el-form>
</div>
</template>

<script>
import axios from "axios";

export default {
  name: "Project_set",
  data(){
    return{
       form_data:{
                   name:'',
                   desc:'',
                   mock:'',
                   priviate:'',
                   power:[],
                   bus_type:'',
                   P_data:'',
                   L_data:'',
                   sign:'',
                },

          }
      },

  mounted() {
    axios.get('http://localhost:8000/get_project_detail/',{
      params:{
        id:this.project_id
      }
    }).then(res=>{
      this.form_data=res.data
    })
  },
  props:['project_id'],
  methods:{
    Save_project: function () {
          axios.post('http://localhost:8000/save_project/', this.form_data).then(
          this.$message({
            message: "保存成功！",
            type: "success",
          })
      )

        }



  },
}
</script>

<style scoped>

</style>