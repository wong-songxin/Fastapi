from .views.views import router as main_router
from fastapi import APIRouter
home_router=APIRouter()
home_router.include_router(main_router,prefix='/main',tags=['首页核心接口'])