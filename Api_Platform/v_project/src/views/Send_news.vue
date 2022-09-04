<template>
  <div style="height: 100%">
    <el-container style="height: 100%">
      <el-aside width="200px">
        <Menu></Menu>
      </el-aside>
      <el-main>
        <h1>消息页面</h1>
            <el-input
                type="textarea"
                :rows="5"
                placeholder='请输入内容'
                v-model="content">
            </el-input>
        <br>
        <br>
          <el-autocomplete
            class="inline-input"
            v-model="state"
            :fetch-suggestions="querySearch"
            placeholder="请输入接受消息的用户名"
            @select="handleSelect"
            :trigger-on-focus="true"
            style="float: left;width: 500px"
          >
            <template slot-scope="{item}">
              <div style="color: #0d0e0e"><strong>用户名：{{item.username}}</strong></div>
              <img onerror="this.src='/static/user_avatar/默认头像.jpg'" class="avatar" style="float: left;width: 50px;height: 50px" :src="'/static/user_avatar/userImage_'+item.id+'.jpg'" alt="">
              <span>【ID：{{item.id}}】</span>
              <span>【职位：{{item.first_name}}】</span>
              <el-divider></el-divider>
            </template>
          </el-autocomplete>&nbsp;
        <el-button @click="send_news"  type="primary" plain="">发送按钮</el-button>
        <br>
        <br>
        <el-card class="box-card" style="min-width:-webkit-calc(100% - 200px);overflow-y: auto;min-height:-webkit-calc(100% - 300px)">
                  <div slot="header" class="clearfix">
                    <span>消息历史记录</span>

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
  name: "Send_news",
  data() {
    return {
      content:'',
      user_info: [],
      state: '',
      user_id:'',
      news:[],
    };

  },
  methods: {
      querySearch(queryString, cb) {
        var user = this.user_info;
        var results = queryString ? user.filter(this.createFilter(queryString)) : user;
        // 调用 callback 返回建议列表的数据
        cb(results);
      },
      createFilter(queryString) {
        return (user) => {
          return (user.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
        };
      },
      loadAll() {
        return []
      },
     handleSelect(item) {
        this.user_id=item.id;
        console.log(item);
      },
     send_news(){
      axios.post("http://localhost:8000/send_news/",{'content':this.content,'user_id':this.user_id}).then(res=>{
        this.$message({
          message:'发送消息成功',
          type:"success"
        })
      })
    },

  },

  components: {
    Menu,
  },
  mounted() {
   axios.get('http://localhost:8000/get_to_user_list/').then(res => {
      this.user_info = res.data.to_user_list;
      this.news = res.data.news;
    })
  }
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