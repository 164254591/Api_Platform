<template>
  <div>
    <el-card id='right_id' style="float:right;width:-webkit-calc(100% - 350px);">
      <div v-if="right_api">
        <el-button size="mini" type="primary">发送</el-button>
        <el-button size="mini" type="primary">保存</el-button>
        &#12288;<br><br>
        <span>接口ID:{{ setting_api.id }}</span><br><br>
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
                <el-tab-pane label="none" name="none"><h2 style="text-align: center;color: darkgrey">不传任何参数</h2>
                </el-tab-pane>
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
                  <el-select v-model="setting_api.methods" style="z-index:999;position:fixed;right:42px;width: 130px"
                             placeholder="Text">
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
                  <el-input type="textarea" :rows="6" style="width: 65%" placeholder="QUERY"></el-input>
                  <el-input type="textarea" :rows="6" style="width: 35%" placeholder="GRAPHQL VARIABLES"></el-input>
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
      <div v-if="right_configure">

        <el-button size="mini" type="primary" @click="save_configure">Save</el-button>
        <el-button size="mini" type="text" @click="up_configure">up</el-button>
        <el-button size="mini" type="text" @click="down_configure">down</el-button>
        &#12288 <span style="float:right;">配置ID: {{ setting_configure.id }}</span>
        <br>
        &#12288 <span>执行时机：</span>
        <el-select v-model="setting_configure.do_time" placeholder="请选择" style="width: 90px">
          <el-option label="before" value="before"></el-option>
          <el-option label="after" value="after"></el-option>
        </el-select>
        &#12288 <span>配置名称：</span>
        <el-input style="width:-webkit-calc(100% - 299px)" v-model="setting_configure.label"></el-input>
        <br><br>
        <el-tabs v-model="setting_configure.method" @tab-click="choose_configure_method" tab-position="left" style="height: 100%">
<!--          <el-tab-pane label="仅运行">-->
<!--            <span class="smallfont">帮助：选中此项后，其他配置不再运行！</span>-->
<!--          </el-tab-pane>-->
          <el-tab-pane name="断言" label="断言">
            <el-select v-model="setting_configure.select" style="width: 120px">
              <el-option label="全值检索" value="全值检索"></el-option>
              <el-option label="正则匹配" value="正则匹配"></el-option>
              <el-option label="路径匹配" value="路径匹配"></el-option>
              <el-option label="SQL断言" value="SQL断言"></el-option>
            </el-select>
            <el-input v-model="setting_configure.value" placeholder="请输入表达式、sql语句" style="width: -webkit-calc(100% - 175px )"></el-input>
            <br>
            <p>帮助</p>
            <p>1.全值检索：在整个返回值当中，是否存在目标字符串。（.find()） * </p>
            <p>2.正则匹配：需要用户写左边界右边界和匹配正则表达式。也是只检索字符串。**</p>
            <p>3.路径匹配：用户写路径和目标的类型和值。* ** （只能是json返回值才可用）</p>
            <p>4.sql断言：用户写sql原生语句和目标值。* * *</p>
            <p>例子：{"errorCode":200,"data":[{"name":"lisi"},{"name":"zhangsan"},{"name":"wang"}]}
            <p>&#12288;全值检索：zhangsan</p>
            <p>&#12288;正则匹配：name":"(.*?)"}==zhangsan</p>
            <p>&#12288;路径匹配：["data"][1]["name"]=="zhangsan"</p>
            <p>&#12288;sql断言：select name from 表 where id=5; == "zhangsan"</p>
            <p>&#12288;sql断言：select name from 表 where name='zhangsan'; (结果是否为0)</p>

          </el-tab-pane>
          <el-tab-pane name="提取" label="提取">
            <el-select v-model="setting_configure.select" style="width: 120px">
              <el-option label="路径提取" value="路径提取"></el-option>
              <el-option label="正则提取" value="正则提取"></el-option>
              <el-option label="sql提取" value="sql提取"></el-option>
            </el-select>
            <el-input v-model="setting_configure.value" placeholder="请输入表达式、sql查询语句" style="width: -webkit-calc(100% - 175px )"></el-input>
            <br>
            <p>帮助：</p>
            <p>1.路径提取：用户写变量名=路径。仅限json</p>
            <p>2.正则提取：用户写变量名=左边界(.*?)右边界</p>
            <p>3.sql提取：用户写变量名=sql select 查询语句 ，还要加下标。（默认0）</p>

          </el-tab-pane>
          <el-tab-pane name="SQL增删改" label="SQL增删改">
            <el-input type="textarea" :rows="5" v-model="setting_configure.value" placeholder="请输入需要执行的sql语句"></el-input>
            <br>
            <p>帮助：</p>
            <p>一般用来执行某个特殊的需求，如修改、增加、删除等。用户手写sql语句即可，没有返回结果</p>
          </el-tab-pane>
          <el-tab-pane name="随机变量" label="随机变量">
            <el-input v-model="setting_configure.value" placeholder="请按照下面要求，输入表达式" ></el-input>
            <br>
            <p>帮助：</p>
            <p>1.常数：a=5, a=8.55, a="呵呵", a=[1,2,3] </p>
            <p>2.随机整数：a=randint(1,10)+2-3-12 #随机生成1-10之内的某个数.</p>
            <p>3.时间戳：a=time.time()</p>
            <p>4.身份证：a=IDcard()</p>
            <p> 5.地址：a=random_adress()</p>
            <p></p>
            <p></p>

          </el-tab-pane>
          <el-tab-pane name="mock" label="mock">
            <el-select v-model="setting_configure.select" style="width: 120px">
              <el-option label="写死返回值" value="写死返回值"></el-option>
              <el-option label="第三方接口" value="第三方接口"></el-option>
            </el-select>
            <el-input type="textarea" :rows="8" v-model="setting_configure.value" placeholder="请输入返回值、接口请求等" ></el-input>
            <br>
            <p>帮助：</p>
            <p>1.选择写死返回值，可直接粘贴返回值到上面的多行文本框，点击保存即可</p>
            <p>2.第三方接口，请依次每行输入：url、header字典、请求体、</p>
          </el-tab-pane>
          <el-tab-pane name="插入参数" label="插入参数">
            <el-select v-model="setting_configure.select" style="width: 150px">
              <el-option label="request_header" value="request_header"></el-option>
              <el-option label="params" value="params"></el-option>
              <el-option label="request_body" value="request_body"></el-option>
            </el-select>
            <el-input  v-model="setting_configure.value" placeholder="请输入表达式" style="width: -webkit-calc(100% - 205px )" ></el-input>
            <br>
            <p>帮助：</p>
            <p>比如：a=55</p>
          </el-tab-pane>
          <el-tab-pane name="加密参数" label="加密参数">
             <el-select v-model="setting_configure.select" style="width: 150px" placeholder="插入位置">
              <el-option label="request_header" value="request_header"></el-option>
              <el-option label="params" value="params"></el-option>
            </el-select>
            <el-input  v-model="setting_configure.value" placeholder="请输入表达式" style="width: -webkit-calc(100% - 205px )" ></el-input>
            <br>
            <p>帮助：</p>
            <p>例如：sign = python能执行的加密算法， 其中可以使用接口的全部位置的参数,函数(md5,shar1)</p>
          </el-tab-pane>
          <el-tab-pane name="草稿" label="草稿">
            <el-input type="textarea" :rows="10" placeholder="请随意使用该文本框"></el-input>
            <p>帮助：临时存放粘贴数据</p>
          </el-tab-pane>


        </el-tabs>
      </div>
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
        :check-strictly="true"
        :default-checked-keys="dck"
        :default-expanded-keys="dek"
        @check-change="handleCheckChange">
      <span slot-scope="{data}">
<!--        <span size="mini">{{ data.label }} &#12288</span>-->
        <span size="mini" v-text="get_label(data.label)"></span>&nbsp;
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
      <el-input v-model="userable_par" type="textarea" :row="5" style="float:right;width: -webkit-calc(100% - 300px)"
                placeholder="当前可用变量"></el-input>
      <el-button size="mini" type="success">执行</el-button> &nbsp;<span>正在执行：</span> <span
        style="color: #42b983">{{ doing_api }}...</span>
      <br>
      <el-button style="margin-top: 10px" size="mini" type="primary">报告</el-button> &nbsp;<span>执行结果：</span>
      <strong><span style="color: darkgreen">成功</span><br></strong>


    </el-card>


  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Project_case",
  data() {
    return {
      right_api: false,
      right_configure: false,
      doing_api: '添加好友',
      userable_par: '',
      setting_api: {},
      setting_configure: {},
      dck: [], // 默认选中的节点
      dek: [], //默认展开的节点
      ref: "tree",
      tableData: [{name: "name", des: 'des'}],
      activeName: "", //body中默认显示哪个tab页
      apis: [
        // {id:1,type:'api',label:'接口1号',children:[{id:'1_1',type:'configure',label:'设置1'},{id:'1_2',type:'configure',label:'设置2'},{id:'1_3',type:'configure',label:'设置3'}]},
      ],
    }
  },
  props: ["project_id",],
  mounted() {
    document.getElementById('right_id').style.minHeight = (document.documentElement.clientHeight - 240).toString() + 'px';
    document.getElementById('right_id').style.maxHeight = (document.documentElement.clientHeight - 240).toString() + 'px';
    document.getElementById('left_div').style.height = (document.documentElement.clientHeight - 286).toString() + 'px'
    axios.get('http://localhost:8000/get_apis/', {
      params: {
        project_id: this.project_id,
      }
    }).then(res => {
      this.apis = res.data
    });
    // 获取选中的接口
    axios.get('http://localhost:8000/get_dck/', {
      params: {
        project_id: this.project_id,
      }
    }).then(res => {
      this.dck = res.data
    });

  },
  methods: {

    up_configure(){
      axios.get('http://localhost:8000/up_configure/',{
        params:{
          configure_id:this.setting_configure.id,
          project_id:this.project_id,
        }
      }).then(res=>{
        this.apis=res.data
      })
    },
    down_configure(){
      axios.get('http://localhost:8000/down_configure/',{
        params:{
          configure_id:this.setting_configure.id,
          project_id:this.project_id,
        }
      }).then(res=>{
        this.apis=res.data
      })
    },
    // get_label(label){
    //   if (label.length>12){
    //     var new_label = label.substring(0,12) + '...'
    //   }
    //   else{
    //     var new_label = label
    //   }
    //   return new_label
    //
    // },
    get_label(label){
      return label.substring(0,12) + ( (label.length>12)?'...':'')
    },
    handleCheckChange(data, checked) {
      console.log(data, checked);
      axios.get('http://localhost:8000/set_dck', {
        params: {
          project: this.project_id,
          dck: this.$refs.tree.getCheckedKeys().toString(),
        }
      }).then(res => {
        this.dck = res.data
      })
    },
    // 如果是接口，则展示接口详情页；否则展示配置详情
    set(data) {
      console.log(data)
      if (data.type == 'api') {
        this.right_api = true;
        this.right_configure = false;
        this.setting_api = data;
      } else {
        this.right_api = false;
        this.right_configure = true;
        this.setting_configure = data;
      }

    },
    // 删除，增加二次确认
    remove(data) {
      if (confirm("确定删除吗？") == false) {
        return
      }
      axios.get('http://localhost:8000/remove_ac', {
        params: {
          project_id: this.project_id,
          id: data.id,
        }
      }).then(res => {
        this.apis = res.data
      })
    },


    v_if(data) {
      if (data.type == 'api') {
        return true
      } else {
        return false
      }
    },
    handleClick(tab, event) {
      console.log(tab, event)
    },
    // 新增配置后，让该接口展开
    add_configure(data) {
      axios.get('http://localhost:8000/add_configure/', {
        params: {
          project_id: this.project_id,
          id: data.id,
        }
      }).then(res => {
        this.apis = res.data;
        this.dek = [data.id];
      })

    },
    add_apis() {
      axios.get('http://localhost:8000/add_apis/', {
        params: {
          project_id: this.project_id,
        }
      }).then(res => {
        this.apis = res.data
      })

    },
    save_configure(){
      axios.post('http://localhost:8000/save_configure/',this.setting_configure).then(res=>{
        this.$message({
          message:'保存成功！',
          type:'success'
        })

      })

    },
    save_api(){

    },
    send_api(){

    },
    run(){

    },
    report(){

    },

    // 选择配置的方法，切换配置tab页时清空之前选择的方式、值
    choose_configure_method(tab,event){
      console.log(tab,event)
      this.setting_configure.select=''
      this.setting_configure.value=''
      this.setting_configure.method=tab.label;
    },


  }
}
</script>

<style scoped>
.smallfont {
  font-size: xx-small;
  color: gray;
}
P{
  font-size: xx-small;
  color: gray;
}
</style>