<template>
  <div style="height: 100%">
    <el-container style="height: 100%">
      <el-aside width="200px">
        <Menu></Menu>
      </el-aside>
      <el-main>
        <h1>公告页面</h1>
            <el-input
                type="textarea"
                :rows="5"
                placeholder='请输入内容'
                v-model="content">
            </el-input>
        <br>
        <br>

        <el-button @click="send_notice"  type="primary" plain="">发送公告</el-button>
        <br>
        <br>
        <el-card class="box-card" style="min-width:-webkit-calc(100% - 200px);overflow-y: auto;min-height:-webkit-calc(100% - 300px)">
                  <div slot="header" class="clearfix">
                    <span>历史公告记录</span>

                  </div>
                  <div v-for="o in news" :key="o" class="text item" >
                    <span style="color: #42b983">发送者：{{ o.from_user_name }}</span>
                    <span style="color: #42b983;font-size: xx-small;"> &nbsp;  发送时间：{{ o.date }}</span>
                    <br><br>
                    <strong>{{o.content}}</strong>
                    <el-divider></el-divider>
                  </div>
            </el-card>

      </el-main>
    </el-container>

  </div>

</template>

<script>
import Menu from "@/components/Menu";
import axios from "axios";

export default {
  name: "Send_notice",
  data() {
    return {
      notice:[],

    };

  },
  methods: {
     send_notice(){
      axios.post("http://localhost:8000/send_notice/",{'content':this.content}).then(res=>{
        this.$message({
          message:'发送公告成功',
          type:"success"
        })
      })
    },

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