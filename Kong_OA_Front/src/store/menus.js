import {defineStore} from 'pinia'
import $cookie from "vue-cookies";

export const definedMenus = defineStore(
    'definedMenus',
    {
        state: () => {
            return {
                editableTabsValue: 'Index', //当前所在那个tab页，组件名字，
                editableTabs: [  //首页一定在这个列表中，因为首页不能关掉
                    {    //总共有多少个Tab页，列表套字典
                    title: '首页',
                    name: 'Index',
                }
                ],

                //1 从来没有发请求获取过动态路由，一开始就是false，加载过就是true
                hasRoutes:false,
                // 2 一旦加载过，左侧菜单列表--》存储
                menuList:[], // 字典套列表---》后端返回的nav对应的数据
                // 3 按钮权限---》后端返回的authoritys对应的数据
                permList:[]

            }
        },
        getters: {},
        actions: {
            addTab(tab) {
                // 去所有tab列表中查找，当前点击的这个菜单，在不在tab列表中
                let index = this.editableTabs.findIndex(e => e.name === tab.name)
                if (index === -1) {
                    this.editableTabs.push({
                        title: tab.title,
                        name: tab.name,
                    });
                } // 不在的情况，我们要增加进去
                // 在的情况，不用增加，只要把当前选中的tab，名字改一下
                this.editableTabsValue = tab.name;
            },

            // 4 我们正常使用pinia，我们不直接操作变量，而是通过方法去操作--》如果是获取{使用}变量，直接用即可
            setMenuList(menus) {
                this.menuList = menus
            },
            setPermList(perms) {
                this.permList = perms
            },
            changeRouteStatus(hasRoutes) {
                this.hasRoutes = hasRoutes
            },


        }
    }
)

// 某个领导：可以看自己部门的数据，还可以看 张三领导的部门数据----》数据权限--》管理员分配后可以看，如果不分配，只能看自己部门


// 问如果部门分父子级别，操作的管理员也多个，属于某个部门的管理员才能查看和操作该下属的，而老板或者更高级的管理员能看到更多不同下属，这样复杂的关系，权限怎么做，查看数据条件怎么写