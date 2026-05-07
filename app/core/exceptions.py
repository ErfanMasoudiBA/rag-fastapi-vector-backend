import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)

# this is for regular http errors like : 404,401,400,403
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    # this kind of error is not apply to inside server and it's about user's command or the Internet
    logger.warning(f"HTTP error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # for the times user inputs are not compatible with our pydantic's schemas
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation error",
            "details": exc.errors(),
        }
    )
    
async def general_exception_handler(request: Request, exc: Exception):
    # for unexpected errors
    # it will write the full traceback
    logger.exception("Unhandled sever error")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error"
        }
    )