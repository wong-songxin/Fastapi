// 首页相关请求
// 前后端打通案例
import request from "../http";
// 命名导出：reqHomeData--》是一个箭头函数
export const reqHomeData=()=>request.get('home/main/cpu')

// 获取服务器性能接口
export const reqServerData=()=>request.get('home/main/info')
