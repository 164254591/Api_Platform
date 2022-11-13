<template>
  <div>
    <el-container style="height: 100%">
      <el-aside width="200px">
        <Menu></Menu>
      </el-aside>
      <el-main>
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
              <span>{{scope.row.status}}</span>
            </template>
          </el-table-column>
          <el-table-column
              prop="next"
              label="下次执行时间"
              width="100%">
          </el-table-column>
          <el-table-column>
            <template slot="header">
              <el-button>新增监控</el-button>
            </template>
            <template slot-scope="scope">
              <el-button size="mini" type="success">开关</el-button>
              <el-button size="mini" type="success">历史报告</el-button>
              <el-button size="mini" type="success">编辑</el-button>
              <el-button size="mini" type="success">删除</el-button>
            </template>
          </el-table-column>

        </el-table>

      </el-main>

     </el-container>



  </div>
</template>

<script>
import axios from "axios";
import Menu from "@/components/Menu";
import Report from "@/components/Report";
export default {
  name: "Monitor",
  data(){
    return{
      monitor_list:[],
      form_data:{

      },


    }
  },
  mounted(){

  },
  methods:{

  },
  components:{
    Menu,
  },
}
</script>

<style scoped>

</style>