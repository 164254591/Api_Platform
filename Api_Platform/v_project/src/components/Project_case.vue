<template>
  <div>
    <el-card id='right_id' style="float:right;width:-webkit-calc(100% - 350px);">
      <div v-if="right_api">
        <el-button @click="send_api" size="mini" type="primary">发送</el-button>
        <el-button @click="save_api" size="mini" type="primary">保存</el-button>
        <el-button @click="up_api" size="mini" type="text">up</el-button>
        <el-button @click="down_api" size="mini" type="text">down</el-button>
        &#12288<span style="font-size: xx-small;color: grey">使用变量请用占位符:{%变量名%}，可用在请求头、url、请求体中</span>
        <span style="float: right">接口ID:{{ setting_api.id }}</span><br><br>
        <el-form ref="form" label-width="100px" label-position="left">
          <el-form-item label="接口名称/描述">
            <el-input v-model="setting_api.label" style="width: 55%"></el-input>
            <el-input v-model="setting_api.des" style="width: 45%"></el-input>
          </el-form-item>
          <el-form-item label="Host">
            <!--            <el-input v-model="setting_api.host"></el-input>-->
            <el-autocomplete
                class="inline-input"
                v-model="setting_api.host"
                :fetch-suggestions="querySearch"
                placeholder="请输入域名"
                @select="handleSelect"
                :trigger-on-focus="true"
                style="float: left;width: 100%"
            >
              <template slot-scope="{item}">
                <div style="color: #0d0e0e"><strong>{{ item.host }}</strong></div>
                <span>【标签：{{ item.type }}】</span>
                <span>【{{ item.des }}】</span>
                <el-divider></el-divider>
              </template>
            </el-autocomplete>


          </el-form-item>
          <el-form-item label="方式/路径">
            <el-select v-model="setting_api.method" style="width: 100px" placeholder="请求方式">
              <el-option label="POST" value="POST"></el-option>
              <el-option label="GET" value="GET"></el-option>
            </el-select>
            <el-input style="width: -webkit-calc(100% - 112px)" v-model="setting_api.path"></el-input>
          </el-form-item>
          <el-tabs type="border-card" v-model="choose_tab_pane">
            <el-tab-pane label="Params">
              <el-table
                  :data="setting_api.params"
                  stripe
                  size="mini"
                  style="width: 100%;overflow-y: auto;min-height: 100%">
                <el-table-column label="参数名" width="180">
                  <template slot-scope="scope">
                    <el-input v-model="scope.row.key"></el-input>
                  </template>
                </el-table-column>
                <el-table-column label="参数值" width="180">
                  <template slot-scope="scope">
                    <el-input v-model="scope.row.value"></el-input>
                  </template>
                </el-table-column>
                <el-table-column label="参数描述" width="180">
                  <template slot-scope="scope">
                    <el-input v-model="scope.row.des"></el-input>
                  </template>
                </el-table-column>
                <el-table-column>
                  <template slot="header">
                    <el-button size="mini" type="primary" @click="add_params">新增</el-button>
                  </template>
                  <template slot-scope="scope">
                    <el-button size="mini" type="danger" @click="del_params(scope.$index)">删除</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
            <el-tab-pane label="Headers">
              <el-table
                  :data="setting_api.headers"
                  stripe
                  size="mini"
                  style="width: 100%;overflow-y: auto;min-height: 100%">
                <el-table-column label="参数名" width="180">
                  <template slot-scope="scope">
                    <el-input v-model="scope.row.key"></el-input>
                  </template>
                </el-table-column>
                <el-table-column label="参数值" width="180">
                  <template slot-scope="scope">
                    <el-input v-model="scope.row.value"></el-input>
                  </template>
                </el-table-column>
                <el-table-column label="参数描述" width="180">
                  <template slot-scope="scope">
                    <el-input v-model="scope.row.des"></el-input>
                  </template>
                </el-table-column>
                <el-table-column>
                  <template slot="header">
                    <el-button size="mini" type="primary" @click="add_headers">新增</el-button>
                  </template>
                  <template slot-scope="scope">
                    <el-button size="mini" type="danger" @click="del_headers(scope.$index)">删除</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
            <el-tab-pane label="Body">
              <el-tabs v-model="setting_api.payload_method" @tab-click="handleClick">
                <el-tab-pane label="none" name="none"><h2 style="text-align: center;color: darkgrey">不传任何参数</h2>
                </el-tab-pane>
                <el-tab-pane label="form-data" name="form-data">
                  <el-table
                      :data="setting_api.payload_fd"
                      stripe
                      size="mini"
                      style="width: 100%;overflow-y: auto;min-height: 100%">
                    <el-table-column label="参数名" width="180">
                      <template slot-scope="scope">
                        <el-input v-model="scope.row.key"></el-input>
                      </template>
                    </el-table-column>
                    <el-table-column label="参数值" width="180">
                      <template slot-scope="scope">
                        <el-input :id="'fd_value_input_'+scope.$index" v-model="scope.row.value"></el-input>
                      </template>
                    </el-table-column>
                    <el-table-column label="文件(上传后参数值不可修改)" width="180">
                      <template slot-scope="scope">
                        <el-upload
                            class="upload-demo"
                            :action="get_action_fd()"
                            :limit="1"
                            name="fd_file"
                            :on-success="upload_fd_file">
                          <el-button @click="set_fd_index(scope.$index)" size="small" type="primary">FILE</el-button>
                        </el-upload>

                      </template>
                    </el-table-column>
                    <el-table-column label="参数描述" width="180">
                      <template slot-scope="scope">
                        <el-input v-model="scope.row.des"></el-input>
                      </template>
                    </el-table-column>
                    <el-table-column>
                      <template slot="header">
                        <el-button size="mini" type="primary" @click="add_payload_fd">新增</el-button>
                      </template>
                      <template slot-scope="scope">
                        <el-button size="mini" type="danger" @click="del_payload_fd(scope.$index)">删除</el-button>
                      </template>
                    </el-table-column>
                  </el-table>
                </el-tab-pane>
                <el-tab-pane label="x-www-form-urlencode" name="x-www-form-urlencode">
                  <el-table
                      :data="setting_api.payload_xwfu"
                      stripe
                      size="mini"
                      style="width: 100%;overflow-y: auto;min-height: 100%">
                    <el-table-column label="参数名" width="180">
                      <template slot-scope="scope">
                        <el-input v-model="scope.row.key"></el-input>
                      </template>
                    </el-table-column>
                    <el-table-column label="参数值" width="180">
                      <template slot-scope="scope">
                        <el-input v-model="scope.row.value"></el-input>
                      </template>
                    </el-table-column>
                    <el-table-column label="参数描述" width="180">
                      <template slot-scope="scope">
                        <el-input v-model="scope.row.des"></el-input>
                      </template>
                    </el-table-column>
                    <el-table-column>
                      <template slot="header">
                        <el-button size="mini" type="primary" @click="add_payload_xwfu">新增</el-button>
                      </template>
                      <template slot-scope="scope">
                        <el-button size="mini" type="danger" @click="del_payload_xwfu(scope.$index)">删除</el-button>
                      </template>
                    </el-table-column>
                  </el-table>
                </el-tab-pane>
                <el-tab-pane label="raw" name="raw">
                  <el-select v-model="setting_api.payload_raw_method"
                             style="z-index:999;position:fixed;right:42px;width: 130px"
                             placeholder="Text">
                    <el-option label="Text" value="Text"></el-option>
                    <el-option label="JavaScript" value="JavaScript"></el-option>
                    <el-option label="JSON" value="JSON"></el-option>
                    <el-option label="XML" value="XML"></el-option>
                    <el-option label="HTML" value="HTML"></el-option>
                  </el-select>
                  <el-input v-model="setting_api.payload_raw" type="textarea" :rows="5"></el-input>
                </el-tab-pane>
                <el-tab-pane label="binary" name="binary">
                  <el-upload
                      class="upload-demo"
                      drag
                      :action="get_action_binary()"
                      :limit="1"
                      name='binary_file'
                      :on-success="upload_binary_file">
                    <i class="el-icon-upload"></i>
                    <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                    <div class="el-upload__tip" slot="tip">只能上传jpg/png文</div>
                  </el-upload>
                </el-tab-pane>
                <el-tab-pane label="GraphQL" name="GraphQL">
                  <el-input v-model="setting_api.payload_GQL_q" type="textarea" :rows="6" style="width: 65%"
                            placeholder="QUERY"></el-input>
                  <el-input v-model="setting_api.payload_GQL_g" type="textarea" :rows="6" style="width: 35%"
                            placeholder="GRAPHQL VARIABLES"></el-input>
                </el-tab-pane>
              </el-tabs>
            </el-tab-pane>
            <el-tab-pane name="Response" label="Response">
              <!--              <el-input v-model="response_data.R" type="textarea" style="height: 100%" :rows="6"></el-input>-->
              <json-viewer :value="get_json()"></json-viewer>
            </el-tab-pane>
            <el-tab-pane label="ResponseData">
              <el-input v-model="response_data.RD" type="textarea" style="height: 100%" :rows="6"></el-input>
            </el-tab-pane>
            <el-tab-pane label="ConfigureResult">
              <el-input v-model="response_data.CR" type="textarea" style="height: 100%" :rows="6"></el-input>
            </el-tab-pane>
          </el-tabs>
        </el-form>
      </div>
      <div v-else-if="right_configure">
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
        <el-tabs v-model="setting_configure.method" @tab-click="choose_configure_method" tab-position="left"
                 style="height: 100%">
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
            <el-input v-model="setting_configure.value" placeholder="请输入表达式、sql语句"
                      style="width: -webkit-calc(100% - 175px )"></el-input>
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
            <p>sql断言：用户必须在语句后写英文分号;</p>
            <p>&#12288;sql断言：select name from 表 where id=5; == "zhangsan(只取第一行第一个单元格数据做验证)"</p>
            <p>&#12288;sql断言：select name from 表 where name='zhangsan'; (结果是否为0)</p>

          </el-tab-pane>
          <el-tab-pane name="提取" label="提取">
            <el-select v-model="setting_configure.select" style="width: 120px">
              <el-option label="路径提取" value="路径提取"></el-option>
              <el-option label="正则提取" value="正则提取"></el-option>
              <el-option label="sql提取" value="sql提取"></el-option>
            </el-select>
            <el-input v-model="setting_configure.value" placeholder="请输入表达式、sql查询语句"
                      style="width: -webkit-calc(100% - 175px )"></el-input>
            <br>
            <p>帮助：</p>
            <p>1.路径提取：用户写变量名=路径。仅限json</p>
            <p>2.正则提取：用户写变量名=左边界(.*?)右边界</p>
            <p>3.sql提取：用户写变量名=sql select 查询语句(只取第一行第一个单元格数据进行赋值)</p>

          </el-tab-pane>
          <el-tab-pane name="SQL增删改" label="SQL增删改">
            <el-input type="textarea" :rows="5" v-model="setting_configure.value"
                      placeholder="请输入需要执行的sql语句"></el-input>
            <br>
            <p>帮助：</p>
            <p>一般用来执行某个特殊的需求，如修改、增加、删除等。用户手写sql语句即可，没有返回结果</p>
          </el-tab-pane>
          <el-tab-pane name="随机变量" label="随机变量">
            <el-input v-model="setting_configure.value" placeholder="请按照下面要求，输入表达式"></el-input>
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
            <el-input type="textarea" :rows="8" v-model="setting_configure.value" placeholder="请输入返回值、接口请求等"></el-input>
            <br>
            <p>帮助：</p>
            <p>1.选择写死返回值，可直接粘贴返回值到上面的多行文本框，点击保存即可</p>
            <p>2.第三方接口，请依次每行输入：url、请求方式、header字典、请求体类型、请求体</p>
            <p>
              如：<br>
              &nbsp; http://www.xxx.com/aaa/bbb?a=1<br>
              &nbsp; post <br>
              &nbsp; {"a":1,"b"：1} <br>
              &nbsp; form-data / x-www-form-urlencode / raw-json / raw-text / raw-html / ram-xml / raw-javascript <br>
              &nbsp; {"username":"zhangsan","userid":45} <br>

            </p>
          </el-tab-pane>
          <el-tab-pane name="插入参数" label="插入参数">
            <el-select v-model="setting_configure.select" style="width: 150px">
              <el-option label="request_header" value="request_header"></el-option>
              <el-option label="params" value="params"></el-option>
              <el-option label="request_body" value="request_body"></el-option>
            </el-select>
            <el-input v-model="setting_configure.value" placeholder="请输入表达式"
                      style="width: -webkit-calc(100% - 205px )"></el-input>
            <br>
            <p>帮助：</p>
            <p>比如：a=55</p>
          </el-tab-pane>
          <el-tab-pane name="加密参数" label="加密参数">
            <el-select v-model="setting_configure.select" style="width: 150px" placeholder="插入位置">
              <el-option label="request_header" value="request_header"></el-option>
              <el-option label="params" value="params"></el-option>
            </el-select>
            <el-input v-model="setting_configure.value" placeholder="请输入表达式"
                      style="width: -webkit-calc(100% - 205px )"></el-input>
            <br>
            <p>帮助：</p>
            <p>例如：sign = python能执行的加密算法， 其中可以使用接口的全部位置的参数,函数(hashlib.md5(),hashlib.shar1())</p>
            <p>定制算法：sign = make_sign()</p>
          </el-tab-pane>
          <el-tab-pane name="草稿" label="草稿">
            <el-input type="textarea" :rows="10" placeholder="请随意使用该文本框"></el-input>
            <p>帮助：临时存放粘贴数据</p>
          </el-tab-pane>


        </el-tabs>
      </div>
      <div v-else-if="right_report">
        <el-dialog title="报告详情如下：" :visible.sync="dialogFormVisible3" width="90%">
          <el-collapse v-for="i in apis_result">
            <el-collapse-item >
              <template slot="title">
                <strong  :style="{color:getColor(i.result)}">{{i.label}}</strong>
              </template>
              <span style="color: grey">【接口执行结果】：</span><strong>{{i.result}}</strong><br>
              <span style="color: grey">【HttpStatus】：</span><strong>{{i.status_code}}</strong><br>
              <span style="color: grey">【请求类型】：</span><strong>{{i.method}}</strong><br>
              <span style="color: grey">【请求URL】：</span><strong>{{i.url}}</strong><br>
              <span style="color: grey">【请求头】：</span><strong>{{i.request_headers}}</strong><br>
              <span style="color: grey">【请求体】：</span><strong>{{i.payload}}</strong><br>
              <span style="color: grey">【请求体类型】：</span><strong>{{i.payload_method}}</strong><br>
              <span style="color: grey">【请求体raw类型】：</span><strong>{{i.payload_raw_method}}</strong><br>
              <span style="color: grey">【返回头】：</span><strong>{{i.response_header}}</strong><br>
              <span style="color: grey">【返回体】：</span><strong>{{i.R}}</strong><br>
              <span style="color: grey">【配置执行结果】：</span><strong>{{i.CR}}</strong><br>
              <span style="color: grey">【变量提取结果】：</span><strong>{{i.TQ}}</strong><br>





            </el-collapse-item>
          </el-collapse>

        </el-dialog>

        <el-button style="float: right" type="danger" @click="clear_all_reports">清空报告</el-button>
        <el-table :data="all_reports" stripe style="max-width: 100%;max-height: 500px;overflow-y: auto">
          <el-table-column label="报告id" width="100">
            <template slot-scope="scope">
              <span>{{ scope.row.id }}</span>
            </template>
          </el-table-column>
          <el-table-column label="生成时间" width="200">
            <template slot-scope="scope">
              <span>{{ scope.row.ctime }}</span>
            </template>
          </el-table-column>
          <el-table-column label="总结果" width="200">
            <template slot-scope="scope">
              <span :style="{color:getColor(scope.row.all_result)}">{{ scope.row.all_result }}</span>
            </template>
          </el-table-column>
          <el-table-column>
            <template slot-scope="scope">
              <el-button type="primary" size="mini" @click="look_report_detail(scope.$index)">查看详情</el-button>
            </template>
          </el-table-column>

        </el-table>
      </div>
      <div v-else="">请点击左侧设置节点...</div>
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
        @check-change="handleCheckChange"
        ref="tree"
        :check-strictly="true">
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
      <el-button size="mini" type="success" @click="run">执行</el-button> &nbsp;<span>正在执行：</span>
      <span id='doing_api' style="color: #42b983"></span>
      <br>
      <el-button @click="look_report" style="margin-top: 10px" size="mini" type="primary">报告</el-button> &nbsp;<span>执行结果：</span>
      <strong><span id="end_result" style="color: darkgreen"></span><br></strong>


    </el-card>


  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Project_case",
  data() {
    return {
      apis_result:[],
      dialogFormVisible3:false,
      all_reports: [],
      right_report: false,
      env_list: [],
      fd_index: '',  //fd参数对应行的下标
      choose_tab_pane: '',
      right_api: false,
      right_configure: false,
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
      response_data: {
        R: '',  // Response
        RD: '', // ResponseData
        CR: '', // ConfigureResult
      },
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
    axios.get('http://localhost:8000/get_env_list/').then(res => {
      this.env_list = res.data;
      this.env_info = this.loadAll();
    })

  },
  methods: {
    getColor(result) {
      if (result.toString() == 'true') {
        return 'green'
      } else {
        return 'red'
      }
    },
    look_report_detail(index){
      this.apis_result=[];
      this.dialogFormVisible3=true;
      this.apis_result = this.all_reports[index].api_result;
      // console.log(this.apis_result)
    },
    clear_all_reports() {
      axios.get('/clear_all_reports/', {
        params: {
          project_id: this.project_id
        }
      }).then(res => {
        this.all_reports = []
      })
    },
    look_report() {
      this.right_configure = false;
      this.right_api = false;
      this.right_report = true;
      axios.get('/get_all_reports/', {
        params: {
          project_id: this.project_id
        }
      }).then(res => {
        this.all_reports = res.data
        // console.log(this.all_reports)
      })
    },
    querySearch(queryString, cb) {
      var env = this.env_info;
      var results = queryString ? env.filter(this.createFilter(queryString)) : env;
      // 调用 callback 返回建议列表的数据
      cb(results);
    },
    createFilter(queryString) {
      return (env) => {
        return (env.host.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
      };
    },
    loadAll() {
      return this.env_list
    },
    handleSelect(item) {
      this.setting_api.host = item.host;
    },

    get_action_binary() {
      return process.env.VUE_APP_BASE_URL + '/upload_binary_file/?ApiID=' + this.setting_api.id
    },
    get_action_fd() {
      return process.env.VUE_APP_BASE_URL + '/upload_fd_file/?ApiID=' + this.setting_api.id
    },
    get_json() {
      try {
        return JSON.parse(this.response_data.R)
      } catch (e) {
        return this.response_data.R
      }
    },
    // 获取index
    set_fd_index(index) {
      this.fd_index = index;
    },
    upload_fd_file(res, file) {
      var file_name = '*FILE*' + this.setting_api.id + '_' + file.raw.name;
      this.setting_api.payload_fd[this.fd_index].value = file_name;
      document.getElementById('fd_value_input_' + this.fd_index).value = file_name;
      document.getElementById('fd_value_input_' + this.fd_index).disabled = true;

    },
    upload_binary_file(res, file) {
      this.setting_api.payload_binary = this.setting_api.id + '_' + file.raw.name;
    },
    up_api() {
      axios.get('http://localhost:8000/up_api/', {
        params: {
          api_id: this.setting_api.id,
          project_id: this.project_id,
        }
      }).then(res => {
        this.apis = res.data;
        this.right_api = false;
        this.dek = [this.setting_api.id]
      })
    },
    down_api() {
      axios.get('http://localhost:8000/down_api/', {
        params: {
          api_id: this.setting_api.id,
          project_id: this.project_id,
        }
      }).then(res => {
        this.apis = res.data;
        this.right_api = false;
      })
    },
    up_configure() {
      axios.get('http://localhost:8000/up_configure/', {
        params: {
          configure_id: this.setting_configure.id,
          project_id: this.project_id,
        }
      }).then(res => {
        this.apis = res.data;
        this.right_configure = false;
        this.dek = [parseInt(this.setting_configure.id.split('_')[0])] // 将字符串转换成整形
      })
    },
    down_configure() {
      axios.get('http://localhost:8000/down_configure/', {
        params: {
          configure_id: this.setting_configure.id,
          project_id: this.project_id,
        }
      }).then(res => {
        this.apis = res.data;
        this.right_configure = false;
        this.dek = [parseInt(this.setting_configure.id.split('_')[0])] // 将字符串转换成整形
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
    get_label(label) {
      return label.substring(0, 12) + ((label.length > 12) ? '...' : '')
    },
    handleCheckChange(data, checked) {
      console.log(data, checked);
      axios.get('http://localhost:8000/set_dck/', {
        params: {
          project_id: this.project_id,
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
        this.right_report = false;
        this.setting_api = data;
        this.response_data = {
          R: '',  // Response
          RD: '', // ResponseData
          CR: '', // ConfigureResult
        };
        // 获取可用变量
        axios.get('/get_userable_par/', {
          params: {
            api_id: data.id,
            project_id: this.project_id,
          }
        }).then(res => {
          this.userable_par = res.data
        })
      } else {
        this.right_api = false;
        this.right_report = false;
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
        this.apis = res.data;
        this.right_api = false;  // 删除后设置右侧不显示
        this.right_configure = false;
        this.dck.remove(data.id);
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
        this.dek = []
      })

    },
    save_configure() {
      axios.post('http://localhost:8000/save_configure/', this.setting_configure).then(res => {
        this.$message({
          message: '保存成功！',
          type: 'success'
        })

      })

    },
    save_api() {
      axios.post('http://localhost:8000/save_api/', this.setting_api, {
        params: {
          project_id: this.project_id
        }
      }).then(res => {
        this.apis = res.data;
        this.$message({
          message: '保存成功',
          type: 'success'
        })
      })
    },
    send_api() {
      axios.post('http://localhost:8000/send_api/', this.setting_api, {
        params: {
          project_id: this.project_id,
        }
      }).then(res => {
        this.response_data = res.data;
        this.choose_tab_pane = 'Response';
      })

    },
    run() {
      if (confirm('执行大用例之前请确保当前接口或配置的设置已经保存') == false) {
        return
      }
      var end_result = document.getElementById('end_result');
      var doing_api = document.getElementById('doing_api');
      var project_id = this.project_id;
      var t = setInterval(function () {
        axios.get('http://localhost:8000/doing_api/', {
          params: {
            project_id: project_id, // 由于作用域的问题，定时器无法获取this.project_id,所以在外面定义变量var
          }
        }).then(res => {
          doing_api.innerText = res.data
        })
      }, 500)
      axios.get('/run/', {
        params: {
          project_id: this.project_id,
          dck: this.dck.toString(),
        }
      }).then(res => {
        clearInterval(t);
        end_result.innerText = res.data;
        if (res.data == 'True') {
          end_result.style.color = 'green'
        } else {
          end_result.style.color = 'red'
        }
        doing_api.innerText = '全部执行完毕'
      })
    },

    report() {

    },

    // 选择配置的方法，切换配置tab页时清空之前选择的方式、值
    choose_configure_method(tab, event) {
      console.log(tab, event)
      this.setting_configure.select = ''
      this.setting_configure.value = ''
      this.setting_configure.method = tab.label;
    },
    // 新增参数
    add_params() {
      this.setting_api.params.push({"key": "", "value": ""})
    },
    // 删除参数
    del_params(index) {
      this.setting_api.params.splice(index, 1)
    },
    // 新增参数
    add_headers() {
      this.setting_api.headers.push({})
    },
    // 删除参数
    del_headers(index) {
      this.setting_api.headers.splice(index, 1)
    },
    // 新增参数
    add_payload_fd() {
      this.setting_api.payload_fd.push({})
    },
    // 删除参数
    del_payload_fd(index) {
      this.setting_api.payload_fd.splice(index, 1)
    },
    // 新增参数
    add_payload_xwfu() {
      this.setting_api.payload_xwfu.push({})
    },
    // 删除参数
    del_payload_xwfu(index) {
      this.setting_api.payload_xwfu.splice(index, 1)
    },


  }
}
</script>

<style scoped>
.smallfont {
  font-size: xx-small;
  color: gray;
}

.el-table {
  max-height: 400px;
  overflow-y: scroll;
}

P {
  font-size: xx-small;
  color: gray;
}
</style>