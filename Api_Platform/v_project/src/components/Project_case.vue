<template>
<div>
    <el-card id='right_id' style="float:right;width:-webkit-calc(100% - 350px);">
      <div v-if="right_api">

        <el-button size="mini" type="primary">发送</el-button>
        <el-button size="mini" type="primary">保存</el-button>
        &#12288;<br><br>
        <span>接口ID:{{setting_api.id}}</span><br><br>
        <span>接口名称:</span>
        <el-input style="width: 80%" v-model="setting_api.label"></el-input>

      </div>
      <div v-if="right_configure"><span>配置详情页{{setting_configure.label}}</span></div>
    </el-card>
  <h1>接口用例页 &#12288
    <el-button size="mini" type="primary">新增接口</el-button>
  </h1>
  <el-tree
  id="left_div"
  style="width:300px;overflow-y: auto"
  :data="apis"
  show-checkbox>
    <span slot-scope="{data}">
      <span size="mini">{{data.label}} &#12288</span>
      <el-button
            type="text"
            size="mini"
            @click="() => set(data)"
      style="color: darkturquoise">
            设置
          </el-button>
          <el-button
            type="text"
            size="mini"
            @click="() => remove(data)">
            删除
          </el-button>

    </span>
  </el-tree>


  <el-card style="position: fixed;bottom: 15px;width:-webkit-calc(100% - 240px);min-height:150px;">
    <el-button size="mini" type="success">执行</el-button>
    <el-button size="mini" type="primary">报告</el-button>
    <span style="margin-left: 15px">当前可用变量：</span>
    <el-input v-model="userable_par" type="textarea" :row="5" style="float:right;width: -webkit-calc(100% - 300px)"></el-input>
    <br><br><span>正在执行：</span><span style="color: #42b983">{{doing_api}}...</span>
    <br><span>执行结果：</span><strong><span style="color: darkgreen">成功</span><br></strong>

  </el-card>


</div>
</template>

<script>
export default {
  name: "Project_case",
  data(){
    return{
      right_api:false,
      right_configure:false,
      doing_api:'添加好友',
      userable_par:'',
      setting_api:{},
      setting_configure:{},
      apis:[
          {id:1,type:'api',label:'接口1号',children:[{id:'set_1',label:'设置1'},{id:'set_2',label:'设置2'},{id:'set_3',label:'设置3'}]},
          {id:2,type:'api',label:'接口2号',children:[]},
          {id:3,type:'api',label:'接口3号',children:[]},
          {id:2,type:'api',label:'接口2号',children:[]},
          {id:2,type:'api',label:'接口2号',children:[]},
          {id:3,type:'api',label:'接口3号',children:[]},
          {id:2,type:'api',label:'接口2号',children:[]},
          {id:2,type:'api',label:'接口2号',children:[]},
          {id:3,type:'api',label:'接口3号',children:[]},
          {id:2,type:'api',label:'接口2号',children:[]},
          {id:2,type:'api',label:'接口2号',children:[]},
          {id:3,type:'api',label:'接口3号',children:[]},
          {id:2,type:'api',label:'接口2号',children:[]},
          {id:2,type:'api',label:'接口2号',children:[]},
          {id:2,type:'api',label:'接口2号',children:[]},

        ],
    }
  },
  mounted() {
    document.getElementById('right_id').style.minHeight = (document.documentElement.clientHeight-290).toString()+'px';
    document.getElementById('left_div').style.height= (document.documentElement.clientHeight-334).toString()+'px'
  },
  methods:{
    set(data){
      console.log(data)
      if(data.type=='api'){
        this.right_api=true;
        this.right_configure=false;
        this.setting_api=data;
      }
      else{
        this.right_api=false;
        this.right_configure=true;
        this.setting_configure=data;
      }

    },
    remove(data){

    }
  }
}
</script>

<style scoped>

</style>