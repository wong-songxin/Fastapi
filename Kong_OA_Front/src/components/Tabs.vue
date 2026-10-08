<template>
  <el-tabs v-model="editableTabsValue" type="card" closable @tab-remove="removeTab" @tab-click="clickTab($event)">
    <el-tab-pane
        v-for="(item, index) in editableTabs"
        :key="item.name"
        :label="item.title"
        :name="item.name"
    >

    </el-tab-pane>
  </el-tabs>
</template>

<script setup>
// 点击某个tab页，会路由跳转--》代码控制路由跳转
import {useRouter} from 'vue-router'
let $router=useRouter() //后面跳转路由使用
// 使用pinia存储，有多少个tab页，以及当前哪个tab页是被点击的
import {definedMenus} from "../store/menus.js";
let $store=definedMenus()
// 计算属性-->本质是一个方法--》可以当属性使用，当方法中使用的变量发生变化，这个方法会重新运算，得到新的值
import {computed} from "vue";
// 1 监控当前在哪个tab页上
const editableTabs=computed({
  get(){
      return $store.editableTabs
  },
  set(val){
    $store.editableTabs=val
  },
})
// 2 监控总共有多少个tab页
const editableTabsValue=computed({
  get(){
    return $store.editableTabsValue
  },
  set(val){
    $store.editableTabsValue=val
  },
})


// 3 关闭某个tab页的监控函数
function removeTab(targetName) {
  // 当前所有tab，列表套字典
  let tabs = editableTabs.value;
  // 当前所在tab页
  let activeName = editableTabsValue.value;
  if (activeName === 'Index') { // 如果用户要关Index，是关不掉的
    return
  }

  if (activeName === targetName) {
    // 关掉当前tab，如果有上一个，当前所在tab变成上一个，如果没有上一个，当前所在tab变成它下一个
    tabs.forEach((tab, index) => {
      if (tab.name === targetName) {
        let nextTab = tabs[index + 1] || tabs[index - 1];
        if (nextTab) {
          activeName = nextTab.name;
        }
      }
    });
  }
  editableTabsValue.value = activeName;
  editableTabs.value = tabs.filter(tab => tab.name !== targetName);
  $router.push({name: activeName})

}
// 4 点击某个tab页的监控函数
function clickTab(target){
  $router.push({name:target.props.name})
}

</script>



<style scoped>

</style>