from fastapi import APIRouter

from .datamanager import router as datamanager_router

biz_router = APIRouter()
biz_router.include_router(datamanager_router)
