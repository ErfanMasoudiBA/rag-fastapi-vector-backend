from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.core.config import settings
from app.api.routes.root import router as root_router
from app.api.router import api_router
# import the main class and make an instance of fastapi
app = FastAPI(
    title=settings.app_name,
    # title is the name of the api
    description=settings.app_description,
    version=settings.app_version,
    debug=settings.debug,
    # all of this shows in swagger and openapi schema
)

app.include_router(api_router)