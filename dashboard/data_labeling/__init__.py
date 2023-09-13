from fastapi import APIRouter

from last.services.app import app

from .labeling_router import router

labeling_router = APIRouter()
labeling_router.include_router(router)
app.include_router(labeling_router)
