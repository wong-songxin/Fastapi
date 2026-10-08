from pydantic import BaseModel, Field, ConfigDict
from src.settings import setting
from typing import List, Any, Optional


class LoginRequest(BaseModel):
    username: str
    password: str


class RoleSchema(BaseModel):
    id: int
    name: str

    # 使用pydantic 把对象转成字典，要带它
    model_config = ConfigDict(from_attributes=True)


'''# 部门相关序列化
# 序列化的类--》给前端的
# class DeptOutSchema(BaseModel):
#     id: int
#     pid_id: int | None = None
#     name: str
#     enabled: bool
#     dept_sort: int
#     # 后期还需要动----》有子关系--》递归序列化
#     # children:List['DeptOutSchema']|None=[]
#     children: Any | None = []

#     # 使用pydantic 把对象转成字典，要带它
#     class Config:
#         from_attributes = True

#     # 自定义一个方法来调用-->递归序列化
#     @classmethod
#     async def from_orm_recursive(cls, obj):
#         # 1 这个obj是一个 部门对象--->使用序列化类[DeptOutSchema]--->转成字典
#         # 坑：dept_dict.children-->不能直接转
#         dept_dict = cls.model_validate(obj).model_dump()
#         # 2 查出当前部门所有的子部门对象，把children查出来
#         children = await obj.children.filter(is_delete=False).all()
#         # 3 自己转，然后替换,是字典
#         dept_dict['children'] = [await cls.from_orm_recursive(child) for child in children]
#         # 4 把转完之后的返回
#         return dept_dict


# 反序列化的，前端给我们的
# 序列化的类--》给前端用的
# class DeptInSchema(BaseModel):
#     pid_id: int | None = None
#     name: str
#     enabled: bool
#     sub_count: int | None = None  # 因为前端没带
#     dept_sort: int

#     class Config:
#         from_attributes = True


# class DeptOutTreeSchema(BaseModel):
#     # 序列化时，改别名
#     value: int = Field(alias="id")
#     label: str = Field(alias="name")
#     children: Any | None = []

#     class Config:
#         from_attributes = True

#     @classmethod
#     async def from_orm_recursive(cls, obj):
#         obj_dict = cls.model_validate(obj).model_dump()
#         children = await obj.children.all()
#         obj_dict["children"] = [await cls.from_orm_recursive(child) for child in children]
#         return obj_dict


# 岗位相关
# class JobOutSchema(BaseModel):
#     id: int
#     name: str
#     enabled: bool
#     job_sort: int

#     # 后期还需要动----》有子关系--》递归序列化
#     # 使用pydantic 把对象转成字典，要带它
#     class Config:
#         from_attributes = True


# 反序列化的，前端给我们的
# 序列化的类--》给前端用的
# class JobInSchema(BaseModel):
#     name: str
#     enabled: bool
#     job_sort: int | None = None

#     class Config:
#         from_attributes = True


# 角色相关
# class RoleOutSchema(BaseModel):
#     id: int
#     name: str
#     level: int
#     description: str
#     data_scope: str
#     status: bool

#     # 关联关系：db_table 指定中间表的名字
#     # depts :  Any | None = []
#     menus: Any | None = []

#     class Config:
#         from_attributes = True

#     @classmethod
#     async def from_orm_recursive(cls, obj):
#         obj_dict = cls.model_validate(obj).model_dump()
#         # depts = await obj.depts.all()
#         menus = await obj.menus.all()
#         # obj_dict["depts"] = [DeptOutSchema.model_validate(dept).model_dump() for dept in depts]
#         obj_dict["menus"] = [menu.id for menu in menus]
#         return obj_dict


# class RoleInSchema(BaseModel):
#     name: str
#     level: int
#     description: str
#     data_scope: str
#     status: bool

#     # 关联关系：db_table 指定中间表的名字
#     # depts : list[DeptOutSchema]
#     menus: list[int] | None = []

#     class Config:
#         from_attributes = True


# 菜单相关
# class MenuInSchema(BaseModel):
#     pid_id: int | None = None
#     # sub_count: int | None = None
#     # 0 菜单，1 子菜单，2 按钮
#     type: int | None = None
#     title: str | None = None
#     name: str
#     component: str | None = None
#     menu_sort: int | None = None
#     icon: str | None = None
#     path: str | None = None
#     # i_frame: bool | None = None
#     # cache: bool | None = None
#     # hidden: bool | None = None
#     permission: str | None = None

#     # is_menu: bool | None = None

#     class Config:
#         from_attributes = True


# class MenuOutSchema(BaseModel):
#     id: int
#     pid_id: int | None = None
#     # sub_count: int | None = None
#     # 0 菜单，1 子菜单，2 按钮
#     type: int | None = None
#     title: str | None = None
#     name: str | None = None
#     component: str | None = None
#     menu_sort: int | None = None
#     icon: str | None = None
#     path: str | None = None
#     # i_frame: bool | None = None
#     # cache: bool | None = None
#     # hidden: bool | None = None
#     permission: str | None = None
#     # is_menu: bool | None = None
#     children: Any | None = []

#     class Config:
#         from_attributes = True

#     @classmethod
#     async def from_orm_recursive(cls, obj):
#         obj_dict = cls.model_validate(obj).model_dump()
#         children = await obj.children.filter(is_delete=False).all()
#         obj_dict["children"] = [await cls.from_orm_recursive(child) for child in children]
#         return obj_dict


# class MenuOutTreeSchema(BaseModel):
#     # 序列化时，改别名
#     value: int = Field(alias="id")
#     label: str = Field(alias="title")
#     children: Any | None = []

#     class Config:
#         from_attributes = True

#     @classmethod
#     async def from_orm_recursive(cls, obj):
#         obj_dict = cls.model_validate(obj).model_dump()
#         children = await obj.children.all()
#         obj_dict["children"] = [await cls.from_orm_recursive(child) for child in children]
#         return obj_dict


# 给用户选择部门页面使用的序列化类
# class DeptOutUserSchema(BaseModel):
#     # 序列化时，改别名
#     id: int
#     label: str = Field(alias="name")
#     children: Any | None = []
#     class Config:
#         from_attributes = True

# class DeptSchema(BaseModel):
#     id: int
#     name: str

#     # 使用pydantic 把对象转成字典，要带它
#     class Config:
#         from_attributes = True


# class JobSchema(BaseModel):
#     id: int
#     name: str

#     # 使用pydantic 把对象转成字典，要带它
#     class Config:
#         from_attributes = True


# class UserSchema(BaseModel):
#     id: int
#     username: str
#     nick_name: str
#     gender: int
#     avatar: str  # 都带一个固定前缀
#     email: str
#     phone: str
#     is_active: bool
#     roles_detail: Any | None = []

#     roles: Any | None = []
#     dept_id: int | None = []
#     job: Any | None = []

#     # dept:DeptSchema|None=None
#     # job:List[JobSchema]|None=[]

#     # 使用pydantic 把对象转成字典，要带它
#     class Config:
#         from_attributes = True

#     @classmethod
#     async def from_common_orm(cls, obj):
#         obj_dict = cls.model_validate(obj).model_dump()
#         obj_dict['avatar'] = f"http://{setting.APP_HOST}:{setting.APP_PORT}/media/{obj_dict['avatar']}"  # 在某个字段前后加固定的
#         roles = await obj.roles.all()
#         obj_dict['roles_detail'] = [{'id': role.id, 'name': role.name} for role in roles]
#         obj_dict['roles'] = [role.id for role in roles]
#         obj_dict['dept_id'] = obj.dept_id
#         obj_dict['job'] = [job.id for job in await obj.job.all()]
#         return obj_dict


# class UserInSchema(BaseModel):
#     username: str
#     nick_name: str
#     gender: int
#     email: str
#     phone: int
#     is_active: bool
#     roles: List[int] | None = []
#     dept_id: int | None = None
#     job: List[int] | None = []


# class MenuPermissionSchema(BaseModel):
#     name: str
#     title: str
#     icon: str | None
#     path: str | None
#     component: str | None
#     children: Any | None

#     class Config:
#         from_attributes = True

#     @classmethod
#     async def from_orm_recursive(cls, obj, menus_ids=None):
#         obj_dict = cls.model_validate(obj).model_dump()
#         if menus_ids:
#             children = await obj.children.filter(type=1, id__in=menus_ids).all()
#         else:
#             children = await obj.children.filter(type=1).all()
#         obj_dict["children"] = [await cls.from_orm_recursive(child) for child in children]
#         return obj_dict
'''


class UserUpdate(BaseModel):
    nick_name: Optional[str] = None
    gender: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None   


class PasswordChange(BaseModel):
    old_password: str = Field(..., description='原密码')
    new_password: str = Field(..., description='新密码')
    confirm_password: str = Field(..., description='确认新密码')


# 部门相关序列化
# 序列化的类--》给前端的
class DeptOutSchema(BaseModel):
    id: int
    pid_id: int | None = None
    name: str
    enabled: bool
    dept_sort: int
    # 后期还需要动----》有子关系--》递归序列化
    # children:List['DeptOutSchema']|None=[]
    children: Any | None = []

    # 使用pydantic 把对象转成字典，要带它
    model_config = ConfigDict(from_attributes=True)

    # 自定义一个方法来调用-->递归序列化
    @classmethod
    async def from_orm_recursive(cls, obj):
        # 1 这个obj是一个 部门对象--->使用序列化类[DeptOutSchema]--->转成字典
        # 坑：dept_dict.children-->不能直接转
        dept_dict = cls.model_validate(obj).model_dump()
        # 2 查出当前部门所有的子部门对象，把children查出来
        children = await obj.children.filter(is_delete=False).all()
        # 3 自己转，然后替换,是字典
        dept_dict['children'] = [await cls.from_orm_recursive(child) for child in children]
        # 4 把转完之后的返回
        return dept_dict


# 反序列化的，前端给我们的
# 序列化的类--》给前端用的
class DeptInSchema(BaseModel):
    pid_id: int | None = None
    name: str
    enabled: bool
    sub_count: int | None = None  # 因为前端没带
    dept_sort: int

    model_config = ConfigDict(from_attributes=True)


class DeptOutTreeSchema(BaseModel):
    # 序列化时，改别名
    value: int = Field(alias="id")
    label: str = Field(alias="name")
    children: Any | None = []

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    async def from_orm_recursive(cls, obj):
        obj_dict = cls.model_validate(obj).model_dump()
        children = await obj.children.all()
        obj_dict["children"] = [await cls.from_orm_recursive(child) for child in children]
        return obj_dict


# 岗位相关
class JobOutSchema(BaseModel):
    id: int
    name: str
    enabled: bool
    job_sort: int

    # 后期还需要动----》有子关系--》递归序列化
    # 使用pydantic 把对象转成字典，要带它
    model_config = ConfigDict(from_attributes=True)


# 反序列化的，前端给我们的
# 序列化的类--》给前端用的
class JobInSchema(BaseModel):
    name: str
    enabled: bool
    job_sort: int | None = None

    model_config = ConfigDict(from_attributes=True)


# 角色相关
class RoleOutSchema(BaseModel):
    id: int
    name: str
    level: int
    description: str
    data_scope: str
    status: bool

    # 关联关系：db_table 指定中间表的名字
    # depts :  Any | None = []
    menus: Any | None = []

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    async def from_orm_recursive(cls, obj):
        obj_dict = cls.model_validate(obj).model_dump()
        # depts = await obj.depts.all()
        menus = await obj.menus.all()
        # obj_dict["depts"] = [DeptOutSchema.model_validate(dept).model_dump() for dept in depts]
        obj_dict["menus"] = [menu.id for menu in menus]
        return obj_dict


class RoleInSchema(BaseModel):
    name: str
    level: int
    description: str
    data_scope: str
    status: bool

    # 关联关系：db_table 指定中间表的名字
    # depts : list[DeptOutSchema]
    menus: list[int] | None = []

    model_config = ConfigDict(from_attributes=True)


# 菜单相关
class MenuInSchema(BaseModel):
    pid_id: int | None = None
    # sub_count: int | None = None
    # 0 菜单，1 子菜单，2 按钮
    type: int | None = None
    title: str | None = None
    name: str
    component: str | None = None
    menu_sort: int | None = None
    icon: str | None = None
    path: str | None = None
    # i_frame: bool | None = None
    # cache: bool | None = None
    # hidden: bool | None = None
    permission: str | None = None

    # is_menu: bool | None = None

    model_config = ConfigDict(from_attributes=True)


class MenuOutSchema(BaseModel):
    id: int
    pid_id: int | None = None
    # sub_count: int | None = None
    # 0 菜单，1 子菜单，2 按钮
    type: int | None = None
    title: str | None = None
    name: str | None = None
    component: str | None = None
    menu_sort: int | None = None
    icon: str | None = None
    path: str | None = None
    # i_frame: bool | None = None
    # cache: bool | None = None
    # hidden: bool | None = None
    permission: str | None = None
    # is_menu: bool | None = None
    children: Any | None = []

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    async def from_orm_recursive(cls, obj):
        obj_dict = cls.model_validate(obj).model_dump()
        children = await obj.children.filter(is_delete=False).all()
        obj_dict["children"] = [await cls.from_orm_recursive(child) for child in children]
        return obj_dict


class MenuOutTreeSchema(BaseModel):
    # 序列化时，改别名
    value: int = Field(alias="id")
    label: str = Field(alias="title")
    children: Any | None = []

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    async def from_orm_recursive(cls, obj):
        obj_dict = cls.model_validate(obj).model_dump()
        children = await obj.children.all()
        obj_dict["children"] = [await cls.from_orm_recursive(child) for child in children]
        return obj_dict


# 给用户选择部门页面使用的序列化类
# class DeptOutUserSchema(BaseModel):
#     # 序列化时，改别名
#     id: int
#     label: str = Field(alias="name")
#     children: Any | None = []
#     class Config:
#         from_attributes = True

class DeptSchema(BaseModel):
    id: int
    name: str

    # 使用pydantic 把对象转成字典，要带它
    model_config = ConfigDict(from_attributes=True)


class JobSchema(BaseModel):
    id: int
    name: str

    # 使用pydantic 把对象转成字典，要带它
    model_config = ConfigDict(from_attributes=True)


class UserSchema(BaseModel):
    id: int
    username: str
    nick_name: str
    gender: str
    avatar: str  # 都带一个固定前缀
    email: str
    phone: str
    is_active: bool
    roles_detail: Any | None = []

    roles: Any | None = []
    dept_id: int | None = []
    job: Any | None = []

    # dept:DeptSchema|None=None
    # job:List[JobSchema]|None=[]

    # 使用pydantic 把对象转成字典，要带它
    model_config = ConfigDict(from_attributes=True)

    @classmethod
    async def from_common_orm(cls, obj):
        obj_dict = cls.model_validate(obj).model_dump()
        obj_dict['avatar'] = f"http://{setting.APP_HOST}:{setting.APP_PORT}/media/{obj_dict['avatar']}"  # 在某个字段前后加固定的
        roles = await obj.roles.all()
        obj_dict['roles_detail'] = [{'id': role.id, 'name': role.name} for role in roles]
        obj_dict['roles'] = [role.id for role in roles]
        obj_dict['dept_id'] = obj.dept_id
        obj_dict['job'] = [job.id for job in await obj.job.all()]
        return obj_dict


class UserInSchema(BaseModel):
    username: str
    nick_name: str
    gender: int
    email: str
    phone: int
    is_active: bool
    roles: List[int] | None = []
    dept_id: int | None = None
    job: List[int] | None = []


class MenuPermissionSchema(BaseModel):
    name: str
    title: str
    icon: str | None
    path: str | None
    component: str | None
    children: Any | None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    async def from_orm_recursive(cls, obj, menus_ids=None):
        obj_dict = cls.model_validate(obj).model_dump()
        if menus_ids:
            children = await obj.children.filter(type=1, id__in=menus_ids).all()
        else:
            children = await obj.children.filter(type=1).all()
        obj_dict["children"] = [await cls.from_orm_recursive(child) for child in children]
        return obj_dict
