from fastapi import FastAPI

from app.core.config import settings
from app.api.router import api_router

from fastapi.staticfiles import StaticFiles
from app.core.logging import setup_logging
# import the main class and make an instance of fastapi

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)

from app.api.routes.ingestion import router as ingestion_router
from app.api.routes.embedding import router as embedding_router


setup_logging()

app = FastAPI(
    title=settings.app_name,
    # title is the name of the api
    description=settings.app_description,
    version=settings.app_version,
    debug=settings.debug,
    # all of this shows in swagger and openapi schema
    docs_url=None,
    redoc_url=None,
)

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)


app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(api_router)

app.include_router(ingestion_router)
app.include_router(embedding_router)