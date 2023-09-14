from fastapi import APIRouter

from .datamanager import router as datamanager_router
from .eval_model import router as eval_model_router
from .dataset import router as dataset_router

biz_router = APIRouter()
biz_router.include_router(datamanager_router)
biz_router.include_router(eval_model_router)
biz_router.include_router(dataset_router)
