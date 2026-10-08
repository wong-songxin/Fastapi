import axios from "axios";
import {ElMessage} from "element-plus";
import $cookie from 'vue-cookies'

import {ElLoading} from 'element-plus'

let loadingInstance
// 1 基本配置
const request = axios.create({
    // 基础配置：访问地址，编码格式，超时时间。。。
    baseURL: 'http://127.0.0.1:8080/api/v1/', // 后期上线，只要变这里就可以来了
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json; charset=utf-8'
    }
})


// 2 请求拦截器--》所有请求发送之前会执行
request.interceptors.request.use(config => {
    // 创建一个加载组件---》可以在请求拦截器中根据请求地址，排除一些接口
    loadingInstance = ElLoading.service({
        lock: true,
        text: '加载中...',
        background: 'rgba(0, 0, 0, 0.5)'
    })
    // 2.1 从cookie中取出用户的登录信息，如果有，就放在请求头中携带
    let token = $cookie.get('token')
    if (token) {
        config.headers.Authorization = 'Bearer ' + token
    }
    return config

})

//3  响应拦截器
request.interceptors.response.use(
    // 3.0  成功情况：100或非100，请求接口成功
    response => {

        //3.1 response 后端接口返回的响应对象：响应头，响应体，响应状态码
        let res = response.data  // 真正的响应体
        // 加载组件销毁
        if (loadingInstance) {
            loadingInstance.close();
        }
        if (res.code == 100) {
            //3.2 请求成功，正常返回
            return res
        } else {
            // 3.3没成功，弹提示
            ElMessage({
                message: !res.msg ? '服务器异常，请联系系统管理员' : res.msg,
                type: 'warning',
                plain: true,
            })
            return Promise.reject(response.data.msg)
        }
    },
    // 3.2 请求接口失败：超时了，没网。。。
    error => {
        if (loadingInstance) {
            loadingInstance.close();
        }
        ElMessage({
            message: '服务器异常，请联系系统管理员',
            type: 'error',
            plain: true,
        })
        return Promise.reject(new Error(error.message))
    }
)

// 4 把请求对象，导出
export default request