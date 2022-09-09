<template>
  <div class="home" style="height: 100%">
    <el-container style="height: 100%">
      <el-aside width="200px">
        <Menu></Menu>
      </el-aside>
      <el-container>

      <el-main>
        <span style="float: right">项目id：{{ $route.query.project_id }}</span>
        <el-tabs v-model="tab_name">
          <el-tab-pane label="项目设置" name="first">
            <Project_set :project_id="$route.query.project_id"></Project_set>
          </el-tab-pane>
          <el-tab-pane label="接口用例" name="second">
            <Project_case :project_id="$route.query.project_id"></Project_case>
          </el-tab-pane>
        </el-tabs>
      </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import Menu from "@/components/Menu";
import Project_set from "@/components/Project_set";
import Project_case from "@/components/Project_case";
import axios from "axios";

export default {
  name: "Project_list",
  data() {
    return {
    tab_name:'first',
    }
  },
  methods: {

  },
  mounted() {

  },
  components: {
    Menu,
    Project_set,
    Project_case,
  },
}
</script>

<style scoped>
.el-header {
  background-color: #B3C0D1;
  color: #333;
  height: 80px;
}

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