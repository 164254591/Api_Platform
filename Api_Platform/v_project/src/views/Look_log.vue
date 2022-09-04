<template>
  <div style="height: 100%">
    <el-container style="height: 100%">
      <el-aside width="200px">
        <Menu></Menu>
      </el-aside>
      <el-main>
        <h1>查看日志</h1>
           <span style="font-size: xx-small;color: gray">最近1000行日志</span>
        <el-input type="textarea" :rows="25" readonly v-model="log_data.logs"></el-input>
        <br>
        <br>
        错误数：<strong style="color: red"> {{log_data.error_count}}</strong>
        <br>
        错误行：<strong style="color: red"> {{log_data.error_lines}}</strong>
        <el-divider></el-divider>
        <br>
        警告数：<strong style="color: red"> {{log_data.waring_count}}</strong>
        <br>
        警告行：<strong style="color: red"> {{log_data.waring_lines}}</strong>
        <el-divider></el-divider>

      </el-main>
    </el-container>

  </div>

</template>

<script>
import Menu from "@/components/Menu";
import axios from "axios";

export default {
  name: "Look_log",
  data() {
    return {
      log_data:{
        logs:'',
        error_count:0,
        error_lines:[],
        waring_count:0,
        waring_lines:[],
      }


    };

  },
  methods: {

  },
  mounted() {
    axios.get("http://localhost:8000/look_log/").then(res=> {
      this.log_data = res.data
    })
  },
  components: {
    Menu,
  },

}
</script>

<style scoped>
.el-aside {
  background-color: #D3DCE6;
  color: #333;
  text-align: center;
  line-height: 200px;

}

.el-main {
  background-color: white;
  color: #333;
  text-align: left;
  line-height: 25px;
}

</style>