import jwt
from fastapi import APIRouter

from ..models import UserInfo, Job, Roles
from src.utils.common_exception import LoginException, AuthException
from ..core import create_access_token, authenticate_user
from src.utils.common_response import APIResponse
from ..schemas import LoginRequest, UserInSchema, UserUpdate, PasswordChange
from fastapi import Depends
from ..core import get_current_user
from ..query_params import UserQueryParams, PaginationQueryParams
from typing import List
from ..schemas import UserSchema
from src.utils.common_response import PaginationResponse
router = APIRouter()
from datetime import datetime
#### 1 用户登录
@router.post('/login', description="登录接口")
async def login(login_request: LoginRequest):
    user: UserInfo = await authenticate_user(login_request.username, login_request.password)
    if not user:
        raise LoginException()
    token = create_access_token(data={'username': user.username})
    return APIResponse(username=user.username, avatar=user.avatar, token=token)


## 2 查询所有用户接口--带分页--带过滤
@router.get("/users", description="查询所有用户")
async def get_user_list(
        page_query: PaginationQueryParams = Depends(),  # 查询分页参数，强行转成PaginationQueryParams的对象：page,page_size...
        user_query: UserQueryParams = Depends(),  # 查询用户参数:根据用户名，用户中文名，是否活跃状态 去查询用户
        user: UserInfo = Depends(get_current_user)
):
    search = user_query.to_query_params()  # {nick_name__icontains:刘}
    users = await UserInfo.filter(**search).filter(is_delete=False).all().prefetch_related("roles", 'dept',
                                                                                           'job')  # users=await UserInfo.filter(nick_name__contains='刘').all()
    # 序列化 Pydantic
    user_dicts = [await UserSchema.from_common_orm(user) for user in users]
    # 返给前端(分页的响应对象)
    return PaginationResponse(data=user_dicts, page=page_query.page, page_size=page_query.page_size)


## 3 根据用户id查询用户详情接口
@router.get('/users/{user_id}', description="查询单个用户")
async def get_user_info(
        user_id: int,
        user: UserInfo = Depends(get_current_user)
):
    # 根据用户id，拿到用户
    user = await UserInfo.filter(id=user_id).prefetch_related("roles", 'dept', 'job').first()
    # 使用pydantic 序列化
    if user:
        user_dict = await UserSchema.from_common_orm(user)
        return APIResponse(result=user_dict)
        # 返回给前端
    else:
        raise Exception('该用户不存在')


## 4 删除用户：单删和多删--请求体中数据格式  [2,3]
@router.delete('/users', description="删除用户接口，单条多条都支持")
async def delete_user(
        ids: List[int],
        user: UserInfo = Depends(get_current_user)
):
    res = await UserInfo.filter(id__in=ids).update(is_delete=True,
                                                   update_by=user.id,
                                                   update_time=datetime.now()
                                                   )  # 软删除，字段控制
    print(res)
    return APIResponse(msg='删除成功')


# 5 新增用户
# @router.post('/users', description="新增用户接口")
# async def create_user(
#         user_in: UserInSchema,
#         user: UserInfo = Depends(get_current_user)
# ):
#     roles = user_in.roles or []
#     jobs = user_in.job or []
#     del user_in.roles
#     del user_in.job
#     password = UserInfo.make_password('123456')
#     user_new = await UserInfo.create(**user_in.model_dump(), password=password)
#     await UserInfo.filter(id=user_new.id).update(create_by=user.username,update_time=datetime.now())
#     for role_id in roles:
#         role = await Roles.get(id=role_id)
#         await user_new.roles.add(role)

#     for job_id in jobs:
#         job = await Job.get(id=job_id)
#         await user_new.job.add(job)

#     return APIResponse(msg='创建成功')

# RBAC调试
@router.post('/users')
async def create_user(
        user_in: UserInSchema,
        user: UserInfo = Depends(get_current_user)
):
    print("========== 1 ==========")
    print("user_in =", user_in)
    print("user_in.roles =", user_in.roles)

    roles = user_in.roles or []
    jobs = user_in.job or []

    print("========== 2 ==========")
    print("roles =", roles)
    print("jobs =", jobs)

    del user_in.roles
    del user_in.job

    password = UserInfo.make_password('123456')

    user_new = await UserInfo.create(
        **user_in.model_dump(),
        password=password
    )

    print("========== 3 ==========")
    print("user_new.id =", user_new.id)

    for role_id in roles:
        print("========== 4 ==========")
        print("role_id =", role_id)

        role = await Roles.get(id=role_id)

        print("role =", role)
        print("role.id =", role.id)
        print("role.name =", role.name)

        await user_new.roles.add(role)

        print("========== 5 ==========")
        print("角色关联完成")

    return APIResponse(msg='创建成功')


# 6 修改用户
@router.put('/users/{user_id}', description="修改用户接口")
async def update_user(
        user_id: int,
        user_in: UserInSchema,
        user: UserInfo = Depends(get_current_user)
):
    roles = user_in.roles or []
    jobs = user_in.job or []
    del user_in.roles
    del user_in.job
    await UserInfo.filter(id=user_id).update(**user_in.model_dump())
    user_new = await UserInfo.get(id=user_id)
    await user_new.roles.clear()
    await user_new.job.clear()
    for role_id in roles:
        role = await Roles.get(id=role_id)
        await user_new.roles.add(role)
    for job_id in jobs:
        job = await Job.get(id=job_id)
        await user_new.job.add(job)
    return APIResponse(msg='修改成功')


# 7 重置密码
@router.post('/reset/password/{user_id}', description="重置密码")
async def reset_password(
        user_id: int,
        user: UserInfo = Depends(get_current_user)
):
    await UserInfo.filter(id=user_id).update(password=UserInfo.make_password('123456'))
    return APIResponse(msg='重置密码成功')


# 8 锁定用户 lock
@router.delete('/lock', description="锁定用户")
async def lock_user(
        ids: List[int],
        user: UserInfo = Depends(get_current_user)
):
    await UserInfo.filter(id__in=ids).update(is_active=False)
    return APIResponse(msg='锁定成功')


# 9 显示个人信息
@router.get("/info")
async def get_user_info(
    current_user: UserInfo = Depends(get_current_user)
):
    await current_user.fetch_related("dept", "roles", "job")

    return APIResponse(result={
    "id": current_user.id,
    "username": current_user.username,
    "email": current_user.email,
    "nick_name": current_user.nick_name,
    "gender": current_user.gender,
    "phone": current_user.phone,
    "avatar": current_user.avatar,
    "enabled": current_user.enabled,
    "is_active": current_user.is_active,
    "is_superuser": current_user.is_superuser,

    "dept": (
        {
            "id": current_user.dept.id,
            "name": current_user.dept.name
        }
        if current_user.dept else None
    ),

    "roles": [
        {"id": role.id, "name": role.name}
        for role in await current_user.roles.all()
    ],

    "job": [
        {"id": job.id, "name": job.name}
        for job in await current_user.job.all()
    ]
})

# 10 用户更新个人信息
@router.put('/info', description="修改用户个人信息")
async def update_user_info(
        data: UserUpdate,
        user: UserInfo = Depends(get_current_user)
):
    update_data = data.model_dump(exclude_unset=True)

    await UserInfo.filter(id=user.id).update(
        **update_data
    )

    # 重新查询修改后的用户
    current_user = await UserInfo.get(id=user.id)
    await current_user.fetch_related("dept", "roles", "job")

    return APIResponse(
        msg='修改个人信息成功',
        result={
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "nick_name": current_user.nick_name,
            "gender": current_user.gender,
            "phone": current_user.phone,
            "avatar": current_user.avatar,
            "enabled": current_user.enabled,
            "is_active": current_user.is_active,
            "is_superuser": current_user.is_superuser,

            "dept": (
                {
                    "id": current_user.dept.id,
                    "name": current_user.dept.name
                }
                if current_user.dept else None
            ),

            "roles": [
                {
                    "id": role.id,
                    "name": role.name
                }
                for role in await current_user.roles.all()
            ],

            "job": [
                {
                    "id": job.id,
                    "name": job.name
                }
                for job in await current_user.job.all()
            ]
        }
    )


# 11 用户更新密码
@router.put('/password', description="修改用户密码")
async def change_password(
    data: PasswordChange,
    user: UserInfo = Depends(get_current_user)
):
    # 1. 验证原密码
    if not user.check_password(data.old_password):
        raise AuthException(msg='原密码错误')

    # 2. 验证两次新密码
    if data.new_password != data.confirm_password:
        raise AuthException(msg='两次输入的新密码不一致')

    # 3. 新密码不能和原密码相同
    if data.old_password == data.new_password:
        raise AuthException(msg='新密码不能与原密码相同')

    # 4. 新密码加密
    user.password = UserInfo.make_password(data.new_password)

    # 5. 保存
    await user.save()

    # 6. 返回
    return APIResponse(
        msg='密码修改成功'
    )