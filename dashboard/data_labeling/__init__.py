from fastapi import APIRouter

from .labeling_router import router

labeling_router = APIRouter()
labeling_router.include_router(router)
