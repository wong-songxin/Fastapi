

<template>
  <el-container>
    <el-header style="background-color: rgb(48, 65, 86);color: aliceblue">
      <strong style="float: left;size: 1000px;font-size: 25px">后台管理系统</strong>

      <div class="header-avatar">

        <el-avatar size="medium" src="https://tva1.sinaimg.cn/large/00831rSTly1gd1u0jw182j30u00u043b.jpg"></el-avatar>
        <el-dropdown style="color: aliceblue">
          <span class="el-dropdown-link">
         登录<el-icon class="el-icon--right"><arrow-down/></el-icon>
          </span>

        <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="openUserInfo">
                个人中心
              </el-dropdown-item>
              <el-dropdown-item divided @click="handleLogout">退出</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>

      </div>

    </el-header>

    <el-container>
      <el-aside width="200px">
        <Sidebar></Sidebar>

      </el-aside>
      <el-main>
        <Tabs></Tabs>
        <div style="margin:0 15px">
          <router-view/>
        </div>

      </el-main>
    </el-container>

  </el-container>
</template>

<script setup>
import Sidebar from "../components/Sidebar.vue";

import Tabs from "../components/Tabs.vue";
import {definedUser} from "../store/user.js";
let $store=definedUser()
import { definedMenus } from "../store/menus.js";
let $menusStore = definedMenus();
import {useRouter} from "vue-router";
let $router=useRouter()

function handleLogout(){
  $store.log_out()
  // 路由跳转到登录页面
  $router.push('/login')
}

function openUserInfo() {
  const tab = {
    title: '个人中心',
    name: 'UserInfo'
  };

  $menusStore.addTab(tab);
  $router.push({ name: tab.name });
}

</script>

<style scoped>
.el-container {
  padding: 0;
  margin: 0;
  height: 100%;
}

.header-avatar {
  float: right;
  width: 210px;
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.el-dropdown-link {
  cursor: pointer;
}

.el-header {
  background-color: #17B3A3;
  color: #333;
  text-align: center;
  line-height: 60px;
}

.el-aside {
  background-color: #D3DCE6;
  color: #333;
  line-height: 200px;
}

.el-main {
  color: #333;
  padding: 0;
}

a {
  text-decoration: none;
}
</style>


