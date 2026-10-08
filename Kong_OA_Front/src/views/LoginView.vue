<template>
<div class="main">
    <div>
      <h1>Kong-OA管理系统</h1>
    </div>

    <el-row type="flex" class="row-bg" justify="center">

      <el-col :xl="6" :lg="7">
        <el-image src="../src/assets/img/back1.png" style="height: 300px; width: 400px;"></el-image>
      </el-col>

      <el-col :span="1">
        <el-divider direction="vertical"></el-divider>
      </el-col>


      <el-col :xl="6" :lg="7">
        <el-form label-width="80px">
          <el-form-item style="width: 380px">
            <el-input v-model="loginForm.username" placeholder="请输入用户名">
              <template #prefix>
                <el-icon class="el-input__icon">
                  <user/>
                </el-icon>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item style="width: 380px">
            <el-input v-model="loginForm.password" type="password" placeholder="请输入密码">
              <template #prefix>
                <el-icon class="el-input__icon">
                  <lock/>
                </el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item style="width: 380px">
            <el-button type="primary" @click="Login" style="width: 45%">登陆</el-button>
            <el-button type="danger" style="width: 45%">注册</el-button>
          </el-form-item>
        </el-form>
      </el-col>

    </el-row>

  </div>
</template>


<script setup>

import {ref,reactive} from "vue";
import {ElMessage} from "element-plus";
import {reqLogin} from "../api/system.js";
import {useRouter} from 'vue-router'
import {definedUser} from "../store/user.js";
const $store=definedUser()
let $router=useRouter()
const loginForm=reactive({
  username:'',
  password:''
})

// 1 写个登录函数--》点击登录按钮--》调用后端接口登录
async function Login(){
  // 1.1 判断用户名密码是否输入了，如果是空，不允许提交
  if(loginForm.password&&loginForm.username){
    // 1.2 发送请求登录
    let res=await reqLogin(loginForm.username,loginForm.password)
    // 需要报错到cookie中---》如果用户没登录，访问任何页面都跳转都login
    // 借助于pinia实现
    // $cookie.set('token',res.token)
    $store.set_user({username:res.username,avatar:res.avatar,token:res.token})
    // 1.3 如果正常走过来，说明登录成功--》跳转到首页
    $router.push('/index')
  }else {
         ElMessage({
            message: '用户名或密码必填',
            type: 'error',
            plain: true,
        })
  }
}
</script>


<style scoped>
.main {
  background-color: #2d3a4b;
  height: 100vh;
  width: 100%;
}

.main div {
  display: flex;
  justify-content: center;
  align-items: center;

}

.main h1 {
  font-size: 35px;
  color: white;
  margin-top: 50px;
  margin-bottom: 100px;
}

</style>
