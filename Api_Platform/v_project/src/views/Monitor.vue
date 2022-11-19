<template>
  <div>
    <el-container style="height: 100%">
      <el-aside width="200px">
        <Menu></Menu>
      </el-aside>
      <el-main>
        <h1>线上监控模块（监控或定时等方式执行具体项目大用例）</h1>
        <el-table
            :data="monitor_list"
            stripe
            border
            style="min-height: 100%;min-width: 100%;overflow-y: auto;">
          <el-table-column
              prop="id"
              label="ID"
              width="100%">
          </el-table-column>
          <el-table-column
              prop="label"
              label="名称"
              width="100%">
          </el-table-column>
          <el-table-column
              prop="project_id"
              label="项目id"
              width="100%">
          </el-table-column>
          <el-table-column
              prop="status"
              label="状态"
              width="100%">
            <template slot-scope="scope">
              <span :style="{color:getColor(scope.row.status)}">{{ scope.row.status }}</span>
            </template>
          </el-table-column>
          <el-table-column
              prop="next"
              label="下次执行时间"
              width="160%">
          </el-table-column>
          <el-table-column>
            <template slot="header">
              <el-button @click="add_monitor">新增监控</el-button>
            </template>
            <template slot-scope="scope">
              <el-button @click="change_monitor_status(scope.row.id)" size="mini" type="success">开关</el-button>
              <el-button @click="look_report(scope.row.project_id)" size="mini" type="default">历史报告</el-button>
              <el-button @click="set_monitor(scope.$index)" size="mini" type="default">编辑</el-button>
              <el-button @click="delete_monitor(scope.row.id)" size="mini" type="danger">删除</el-button>
            </template>
          </el-table-column>

        </el-table>

      </el-main>
    </el-container>

    <el-dialog :visible.sync="dialogFormVisible1" width="60%">
      <el-form :model="form_data">
        <el-form-item label="监控名称" label-width="120px">
          <el-input v-model="form_data.label"></el-input>
        </el-form-item>
        <el-form-item label="关联项目id" label-width="120px">
          <el-input v-model="form_data.project_id"></el-input>
        </el-form-item>
        <el-form-item label="监控方式" label-width="120px">
          <el-radio-group v-model="form_data.method" @change="change_jkfs">
            <el-radio label="间隔时间">间隔(分)</el-radio>
            <el-radio label="每日定时">每日定时(24小时制如：17：22)</el-radio>
            <el-radio label="接口触发">接口触发(不可修改)</el-radio>
            <el-radio label="Jenkins语法">Jenkins语法</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="设置值" label-width="120px">
          <el-input v-model="form_data.value">请输入对应的值</el-input>
        </el-form-item>

        <el-form-item label="邮件接收地址" label-width="120px">
          <el-input v-model="form_data.email" placeholder="多个用英文逗号,隔开"></el-input>
        </el-form-item>
        <el-form-item label="开关状态" label-width="120px">
          <el-input v-model="form_data.status" disabled ></el-input>
        </el-form-item>
        <el-form-item label="机器人" label-width="120px">
          <el-input v-model="form_data.robot" ></el-input>
        </el-form-item>
      </el-form>

      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible1=false">取消</el-button>
        <el-button type="primary" @click="save_monitor">保存</el-button>

      </div>

    </el-dialog>

    <el-dialog :visible.sync="dialogFormVisible2">
      <Report :project_id="look_report_project_id" v-if="dialogFormVisible2"></Report>
    </el-dialog>


  </div>
</template>

<script>
import axios from "axios";
import Menu from "@/components/Menu";
import Report from "@/components/Report";

export default {
  name: "Monitor",
  data() {
    return {
      dialogFormVisible1:false,
      dialogFormVisible2:false,
      look_report_project_id: '',
      monitor_list: [],
      form_data: {},


    }
  },
  mounted() {
    axios.get('/get_monitor_list/').then(res => {
      this.monitor_list = res.data
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
    change_jkfs(){
      this.form_data.value=''; // 清空之前的值
       if (this.form_data.method=='接口触发'){
          this.form_data.value = process.env.VUE_APP_BASE_URL+'/run/?project_id='+this.form_data.project_id;
        }

    },
    add_monitor() {
      axios.get('/add_monitor/').then(res => {
        this.monitor_list = res.data;
      })
    },
    change_monitor_status(id) {
      axios.get('/change_monitor_status/', {
        params: {
          id: id
        }
      }).then(res => {
        this.monitor_list = res.data
      })

    },
    look_report(project_id) {
      this.dialogFormVisible2=true;
      this.look_report_project_id = project_id

    },
    set_monitor(index) {
      this.dialogFormVisible1=true;
      this.form_data = this.monitor_list[index];

    },
    delete_monitor(id) {
      axios.get('/delete_monitor/', {
        params: {
          id: id
        }
      }).then(res => {
        this.monitor_list = res.data
      })
    },
    save_monitor(){
      axios.post('/save_monitor/',this.form_data).then(res=>{
        this.monitor_list=res.data;
        this.dialogFormVisible1=false;
      })
    },

  },
  components: {
    Menu,
    Report,
  },
}
</script>

<style scoped>

</style>