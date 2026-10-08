# 菜单相关接口
from fastapi import APIRouter
from ..schemas import MenuInSchema,MenuOutSchema,MenuOutTreeSchema
from ..models import Menu, UserInfo
from ..core import get_current_user
from fastapi import Depends
from typing import List
from src.utils.common_response import APIResponse

router = APIRouter()


# 菜单增
@router.post('/menus', description="菜单新增")
async def add_menu(menu: MenuInSchema,
                   # user: UserInfo = Depends(get_current_user)
                   ):
    await Menu.create(**menu.model_dump())
    return APIResponse()


# 菜单删
@router.delete('/menus', description="删除接口，单条多条都支持")
async def delete_menu(
        ids: List[int],
        # user: UserInfo = Depends(get_current_user)
):
    res = await Menu.filter(id__in=ids).update(is_delete=True)  # 软删除，字段控制
    return APIResponse(msg='菜单删除成功')


# 菜单查所有
## 1 查询所有menu接口----不分页
@router.get("/menus", description="查询所有菜单")
async def get_menu_list():
    menus = await Menu.filter(is_delete=False,pid=None).all().prefetch_related('children')
    # 子序列化
    menu_dicts = [await MenuOutSchema.from_orm_recursive(menu) for menu in menus]
    return APIResponse(results=menu_dicts)



# 菜单查一个
@router.get("/menus/{menu_id}", description="查询菜单详情")
async def get_menu(
        menu_id: int,
        #user: UserInfo = Depends(get_current_user)
):
    menu = await Menu.filter(id=menu_id).prefetch_related('children').first()
    menu_dict = await MenuOutSchema.from_orm_recursive(menu)
    return APIResponse(result=menu_dict)


# 菜单修改
@router.put("/menus/{menu_id}", description="查询菜单详情")
async def update_menu(
        menu_id: int,
        menu: MenuInSchema,
        #user: UserInfo = Depends(get_current_user)
):
    await Menu.filter(id=menu_id).update(**menu.model_dump())
    return APIResponse()


# 查询菜单树
@router.get("/tree/menus", description="查询所有菜单")
async def get_menu_list_tree(
    # user: UserInfo = Depends(get_current_user)
):
    menus = await Menu.filter(is_delete=False,pid=None).all().prefetch_related('children')
    menu_dicts = [await MenuOutTreeSchema.from_orm_recursive(menu) for menu in menus]
    return APIResponse(results=menu_dicts)