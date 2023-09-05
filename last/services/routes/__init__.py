from fastapi import APIRouter

from .others import router as others_router
from .resources import router as resources_router

router = APIRouter()
router.include_router(resources_router)
router.include_router(others_router)
