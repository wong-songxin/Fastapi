

<template>
<h1>我才是真主页</h1>
  <div  class="main">
    <h2>cpu核数为：{{data.cpu_count}}</h2>
    <h2>cpu使用率为:{{data.cpu_percent}}%</h2>
  </div>

  <hr>
  <h1>element-plus的使用</h1>
  <el-button type="danger" @click="showAlert">Success</el-button>
  <el-button type="primary" :icon="Edit" />
  <h1>布局使用</h1>
  <el-row>
    <el-col :span="12">
      <div class="div1" />
    </el-col>
    <el-col :span="12">
      <div class="div2" />
    </el-col>
  </el-row>
</template>

<script setup>
import {ref} from 'vue'



//  前后端打通案例---》使用封装后的axios发送请求
// ----之前-----
// import axios from 'axios'
// const data=ref({})
// axios.get('http://127.0.0.1:8080/api/v1/home/main/cpu').then(res=>{
//   if (res.data.code==100){
//     data.value=res.data.data
//   }
// })
// ----之后-----
const data=ref({})
import {reqHomeData} from '../api/home.js'
async function getHomeData(){
  let res= await reqHomeData()
  data.value = res.data;
}
getHomeData()




import { Delete, Edit, Search, Share, Upload } from '@element-plus/icons-vue'
function showAlert(){
  alert('弹出来了')
}

</script>

<style scoped>
.main{
  background-color: pink;
  height: 200px;
  width: 100%;
}


.div1{
  background-color: red;
  height: 20px;
}
.div2{
  background-color: green;
  height: 20px;
}
</style>
