from fastapi import APIRouter

from .labeling_router import router
from last.services.app import app

labeling_router = APIRouter()
labeling_router.include_router(router)
app.include_router(labeling_router)
