<template>
<div >
    <el-card id='right_id' style="float:right;width:-webkit-calc(100% - 350px);">
      <div v-if="right_api">
        <el-button size="mini" type="primary">发送</el-button>
        <el-button size="mini" type="primary">保存</el-button>
        &#12288;<br><br>
        <span>接口ID:{{setting_api.id}}</span><br><br>
        <el-form ref="form" label-width="80px" label-position="left">
          <el-form-item label="接口名称/描述">
            <el-input v-model="setting_api.label" style="width: 55%"></el-input>
            <el-input v-model="setting_api.label" style="width: 45%"></el-input>
          </el-form-item>

          <el-form-item label="Host">
            <el-input v-model="setting_api.label"></el-input>
          </el-form-item>
          <el-form-item label="方式/路径">
            <el-select v-model="setting_api.methods" style="width: 100px" placeholder="请求方式">
              <el-option label="POST" value="POST"></el-option>
              <el-option label="GET" value="GET"></el-option>
            </el-select>
            &nbsp;
            <el-input style="width: -webkit-calc(100% - 112px)" v-model="setting_api.path"></el-input>
          </el-form-item>

          <el-tabs>
            <el-tab-pane label="Params">
              <el-table
                :data="env_list_data"
                stripe
                size="mini"
                style="width: 100%;overflow-y: auto;min-height: 100%">
              <el-table-column
                  prop="id"
                  label="参数名">
              </el-table-column>
              <el-table-column
                  prop="host"
                  label="参数描述">
              </el-table-column>
                <el-table-column
                  prop="host"
                  label="操作">
              </el-table-column>
              </el-table>
            </el-tab-pane>
            <el-tab-pane label="Headers">请求头</el-tab-pane>
            <el-tab-pane label="Body">
               <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
                <el-tab-pane label="none" name="none"><h2 style="text-align: center;color: darkgrey">不传任何参数</h2></el-tab-pane>
                <el-tab-pane label="form-data" name="form-data">
                  <el-table
                    :data="env_list_data"
                    stripe
                    size="mini"
                    style="width: 100%;overflow-y: auto;min-height: 100%">
                  <el-table-column
                      prop="id"
                      label="参数名">
                  </el-table-column>
                  <el-table-column
                      prop="host"
                      label="参数描述">
                  </el-table-column>
                    <el-table-column
                      prop="host"
                      label="操作">
                  </el-table-column>
                  </el-table>
                </el-tab-pane>
                <el-tab-pane label="x-www-form-urlencode" name="x-www-form-urlencode">
                  <el-table
                    :data="env_list_data"
                    stripe
                    size="mini"
                    style="width: 100%;overflow-y: auto;min-height: 100%">
                  <el-table-column
                      prop="id"
                      label="参数名">
                  </el-table-column>
                  <el-table-column
                      prop="host"
                      label="参数描述">
                  </el-table-column>
                    <el-table-column
                      prop="host"
                      label="操作">
                  </el-table-column>
                  </el-table>
                </el-tab-pane>
                <el-tab-pane label="raw" name="raw">
                  <el-select v-model="setting_api.methods" style="z-index:999;position:fixed;right:42px;width: 130px" placeholder="Text">
                    <el-option label="Text" value="Text"></el-option>
                    <el-option label="JavaScript" value="JavaScript"></el-option>
                    <el-option label="JSON" value="JSON"></el-option>
                    <el-option label="XML" value="XML"></el-option>
                    <el-option label="HTML" value="HTML"></el-option>
                  </el-select>
                  <el-input type="textarea" :rows="5"></el-input>
                </el-tab-pane>
                <el-tab-pane label="binary" name="binary">
                  <el-upload
                    class="upload-demo"
                    drag
                    action="https://jsonplaceholder.typicode.com/posts/"
                    multiple>
                    <i class="el-icon-upload"></i>
                    <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                    <div class="el-upload__tip" slot="tip">只能上传jpg/png文</div>
                  </el-upload>
                </el-tab-pane>
                <el-tab-pane label="GraphQL" name="GraphQL">
                  <el-input type="textarea":rows="6" style="width: 65%" placeholder="QUERY"></el-input>
                  <el-input type="textarea":rows="6" style="width: 35%" placeholder="GRAPHQL VARIABLES"></el-input>
                </el-tab-pane>
              </el-tabs>
            </el-tab-pane>
            <el-tab-pane label="Response">
              <el-input type="textarea" style="height: 100%" :rows="6"></el-input>
            </el-tab-pane>

            <el-tab-pane label="ResquestCode">请求代码</el-tab-pane>
            <el-tab-pane label="ConfigureResult">配置</el-tab-pane>
          </el-tabs>

        </el-form>




      </div>

      <div v-if="right_configure"><span>配置详情页:{{setting_configure.label}}</span></div>
    </el-card>

  <h1>接口用例页 &#12288
    <el-button size="mini" type="primary" @click="add_apis">新增接口</el-button>
  </h1>
  <el-tree
  id="left_div"
  style="width:300px;overflow-y: auto"
  :data="apis"
  show-checkbox
  node-key="id"
  :default-checked-keys="dck"
  :default-expanded-keys="dek"
  @check-change="handleCheckChange">
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
            v-if="v_if(data)"
            type="text"
            size="mini"
            @click="() => add_configure(data)"
            style="color: darkgreen">
            增加
      </el-button>
      <el-button
            type="text"
            size="mini"
            @click="() => remove(data)">
            删除
      </el-button>

    </span>
  </el-tree>


  <el-card style="position: fixed;bottom: 15px;width:-webkit-calc(100% - 240px);min-height:100px;">
    <el-input v-model="userable_par" type="textarea" :row="5" style="float:right;width: -webkit-calc(100% - 300px)" placeholder="当前可用变量"></el-input>
    <el-button size="mini" type="success">执行</el-button> &nbsp;<span>正在执行：</span> <span style="color: #42b983">{{doing_api}}...</span>
    <br>
    <el-button style="margin-top: 10px" size="mini" type="primary">报告</el-button> &nbsp;<span>执行结果：</span> <strong><span style="color: darkgreen">成功</span><br></strong>





  </el-card>


</div>
</template>

<script>
import axios from "axios";
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
      dck:[], // 默认选中的节点
      dek:[], //默认展开的节点
      ref:"tree",
      tableData: [{name:"name",des:'des'}],
      activeName:"", //body中默认显示哪个tab页
      apis:[
          // {id:1,type:'api',label:'接口1号',children:[{id:'1_1',type:'configure',label:'设置1'},{id:'1_2',type:'configure',label:'设置2'},{id:'1_3',type:'configure',label:'设置3'}]},
          // {id:2,type:'api',label:'接口2号',children:[]},
          // {id:3,type:'api',label:'接口3号',children:[]},
          // {id:4,type:'api',label:'接口2号',children:[]},
          // {id:5,type:'api',label:'接口2号',children:[]},
          // {id:6,type:'api',label:'接口3号',children:[]},
          // {id:7,type:'api',label:'接口2号',children:[]},
        ],
    }
  },
  props:["project_id",],
  mounted() {
    document.getElementById('right_id').style.minHeight = (document.documentElement.clientHeight-240).toString()+'px';
    document.getElementById('right_id').style.maxHeight = (document.documentElement.clientHeight-240).toString()+'px';
    document.getElementById('left_div').style.height= (document.documentElement.clientHeight-286).toString()+'px'
    axios.get('http://localhost:8000/get_apis/', {
      params:{
        project_id:this.project_id,
      }
    }).then(res=>{
      this.apis=res.data
    });
    // 获取选中的接口
    axios.get('http://localhost:8000/get_dck/',{
      params:{
        project_id:this.project_id,
      }
    }).then(res=>{
      this.dck=res.data
    });

  },
  methods:{
    handleCheckChange(data, checked) {
        console.log(data, checked);
        axios.get('http://localhost:8000/set_dck',{
          params:{
            project:this.project_id,
            dck:this.$refs.tree.getCheckedKeys().toString(),
          }
        }).then(res=>{
          this.dck=res.data
        })
      },
    // 如果是接口，则展示接口详情页；否则展示配置详情
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
    // 删除，增加二次确认
    remove(data){
      if(confirm("确定删除吗？")==false){return}
      axios.get('http://localhost:8000/remove_ac',{
          params:{
            project_id:this.project_id,
            id:data.id,
          }
        }).then(res=>{
          this.apis=res.data
      })
      },


    v_if(data){
      if(data.type=='api'){
        return true
      }else{
        return false
      }
    },
    handleClick(tab,event){
      console.log(tab,event)
    },
    // 新增配置后，让该接口展开
    add_configure(data){
      axios.get('http://localhost:8000/add_configure/',{
        params:{
          project:this.project_id,
          id:data.id,
        }
      }).then(res=>{
        this.apis=res.data;
        this.dek=[data.id];
      })

    },
    add_apis(){
      axios.get('http://localhost:8000/add_apis/',{
        params:{
          project_id:this.project_id,
        }
      }).then(res=>{
        this.apis=res.data
      })

    },


  }
}
</script>

<style scoped>

</style>