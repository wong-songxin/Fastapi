import {defineStore} from 'pinia'
import $cookie from "vue-cookies";
import {definedMenus} from "./menus.js";
export const definedUser = defineStore(
    'definedUser', //必须唯一
    {
        state: () => { // state中用于定义数据
            return {
                login_user:{
                    username:$cookie.get('username'),
                    avatar:$cookie.get('avatar'),
                    token:$cookie.get('token')
                }
            }
        },
        getters: {
        },
        actions: {
            //1 登录成功，存储登录状态的方法
            set_user(user){
                this.login_user=user
                // 用户信息，放到cookie中
                $cookie.set('username',user.username,'7d')
                $cookie.set('avatar',user.avatar,'7d')
                $cookie.set('token',user.token,'7d')
            },

            // 2 退出，清除登录状态的方法-->本地退出，如果退出需要通知后端，后续需要继续发送网络请求
            log_out(){
                this.login_user={
                    username:'',
                    avatar:'',
                    token:''
                }
                $cookie.remove('username')
                $cookie.remove('avatar')
                $cookie.remove('token')
                // 发送网络请求，告诉服务端xx退出了
               //  删除pinia中存的权限和菜单
                let $store = definedMenus()
                 $store.menuList=[]
                // 按钮权限
                $store.permList=[]
            }
        }
    }
)