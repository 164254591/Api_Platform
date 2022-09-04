<template>
  <div style="height: 100%">
    <el-container style="height: 100%">
      <el-aside width="200px">
        <Menu></Menu>
      </el-aside>
      <el-main>
        <h1>个人信息设置</h1>
        <el-form ref="form" :model="form_data" label-width="100px" :label-position="'right'">
          <el-form-item label="用户名：">
            <el-input v-model="form_data.user_name"></el-input>
          </el-form-item>
          <el-form-item label="密码：">
            <el-input v-model="form_data.password"></el-input>
          </el-form-item>
          <el-form-item label="职称：">
            <el-input v-model="form_data.title"></el-input>
          </el-form-item>
          <el-form-item label="头像：">
            <el-upload
                class="avatar-uploader"
                action="http://localhost:8000/upload_user_avatar/"
                :show-file-list="false"
                :on-success="handleAvatarSuccess"
                :before-upload="beforeAvatarUpload"
                name='user_avatar'>
              <img onerror="this.src='/static/user_avatar/默认头像.jpg'"  v-if="imageUrl" :src="imageUrl" class="avatar">
              <i v-else class="el-icon-plus avatar-uploader-icon"></i>
            </el-upload>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="save_user_detail">保 存</el-button>

          </el-form-item>

        </el-form>
      </el-main>
    </el-container>

  </div>

</template>

<script>
import Menu from "@/components/Menu";
import axios from "axios";

export default {
  name: "User_detail",
  data() {
    return {
      user_list: [],
      form_data: {
        user_id: '',
        user_name: '',
        password: '',
        title: '',

      },
      imageUrl: '',
    };

  },
  methods: {
    save_user_detail() {
      axios.post('http://localhost:8000/save_user_detail/', this.form_data).then(res => {
        this.user_list = res.data
        this.$message({
          message: '保存成功',
          type: 'success',
        })
      })
    },

    handleAvatarSuccess(res, file) {
      this.imageUrl = URL.createObjectURL(file.raw);
    },
    beforeAvatarUpload(file) {
      const isJPG = file.type === 'image/jpeg';
      const isLt2M = file.size / 1024 / 1024 < 2;
      if (!isJPG) {
        this.$message.error('上传头像图片只能是 JPG 格式!');
      }
      if (!isLt2M) {
        this.$message.error('上传头像图片大小不能超过 2MB!');
      }
      return isJPG && isLt2M;
    }
  },
  components: {
    Menu,
  },
  mounted() {
    axios.get('http://localhost:8000/get_user_list/').then(res => {
      this.form_data = res.data
      this.imageUrl = '/static/user_avatar/userimage_' + res.data.user_id + '.jpg'
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

.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.avatar-uploader .el-upload:hover {

  border-color: #409EFF;
}

.avatar-uploader-icon {
  border: 1px dashed #d9d9d9;
  font-size: 28px;
  color: #9d8c94;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}

.avatar {
  width: 178px;
  height: 178px;
  display: block;
}

</style>