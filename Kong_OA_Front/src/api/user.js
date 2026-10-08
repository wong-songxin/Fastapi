import request from "../http";

export const reqUserList = (params) => request.get('system/user/users', {params})

export const reqUserInfo = () => request.get('system/user/info')
// export const reqUpdateUserInfo = () => request.put('system/user/info')
// 修改当前登录用户个人信息
export const reqUpdateUserInfo = (data) => {
    return request.put('system/user/info', data)
}
// 用户修改密码
// 修改当前登录用户密码
export const reqChangePassword = (data) => {
    return request.put('system/user/password', data)
}
export const reqDeleteUser = (ids) => request.delete('system/user/users', {data: ids})

export const reqUser = (id) => request.get(`system/user/users/${id}`)

export const reqUpdateUser = (id, data) => request.put(`system/user/users/${id}`, {...data})
export const reqCreateUser = (data) => request.post(`system/user/users`, {...data})
export const reqResetPassword = (id) => request.post(`system/user/reset/password/${id}`)

export const reqLockUsers = (ids) => request.delete(`system/user/lock`, {data: ids})
