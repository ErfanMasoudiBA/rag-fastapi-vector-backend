from fastapi import APIRouter

from app.api.routes.health import router as health_router
from app.api.routes.root import router as root_router

api_router = APIRouter()
# this router plays the role of router aggregator
# it doesn't define any endpoints, it just gathered other routes

api_router.include_router(root_router)
api_router.include_router(health_router)