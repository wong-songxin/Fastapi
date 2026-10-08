
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.apps.home import home_router
from src.apps.system import system_router
from src.apps.oa import oa_router
from src.utils.common_middelware import add_cors_middleware

from src.utils.common_db import register_mysql
from src.utils.common_exception import register_excepiton
def register_router(app:FastAPI):
    app.include_router(home_router,prefix='/api/v1/home',tags=['首页所有的路由'])
    app.include_router(system_router,prefix='/api/v1/system',tags=['系统所有路由'])
    app.include_router(oa_router,prefix='/api/v1/oa',tags=['oa所有路由'])

def register_middle_ware(app:FastAPI):
    add_cors_middleware(app)
def create_app()->FastAPI:
    # 1 实例化得到app对象
    app=FastAPI()
    # 2  注册路由
    register_router(app)
    # 3 注册中间件
    register_middle_ware(app)
    # 4 注册orm
    register_mysql(app)
    # 5 注册全局异常
    register_excepiton(app)
    # 6 开启media访问-->以后media目录下所有东西，从浏览器可以直接访问到，以后这个文件夹下不能乱放东西
    app.mount('/media',StaticFiles(directory='media'),name='media')
    return app
