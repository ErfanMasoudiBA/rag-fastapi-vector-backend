from fastapi import APIRouter
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html

router = APIRouter(tags=["docs"])

@router.get("/docs", include_in_schema=False)
def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Docs",
        swagger_js_url="/static/swagger/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger/swagger-ui.css",
    )
    

@router.get("/redoc", include_in_schema=False)
def custom_redoc_html():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="RedDoc",
        redoc_js_url="/static/redoc/redoc.standalone.js",
    )