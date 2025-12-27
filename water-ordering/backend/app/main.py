"""网上订水小程序 - 后端主入口"""

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from app.config import get_settings
from app.api import auth, admin_auth, users, products, orders, addresses, payment, upload

settings = get_settings()

app = FastAPI(
    title="网上订水 API",
    description="网上订水小程序后端接口",
    version="1.0.0",
    docs_url=None,
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """统一处理 HTTP 异常，转换为统一响应格式"""
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": 401,
                "message": str(exc.detail) if exc.detail else "未授权，请先登录",
                "data": None
            }
        )
    elif exc.status_code == status.HTTP_403_FORBIDDEN:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": 403,
                "message": str(exc.detail) if exc.detail else "权限不足",
                "data": None
            }
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": str(exc.detail) if exc.detail else "请求失败",
            "data": None
        }
    )


def custom_openapi():
    """自定义 OpenAPI schema，强制使用 3.0.2 版本以兼容 Swagger UI"""
    if app.openapi_schema:
        return app.openapi_schema
    from fastapi.openapi.utils import get_openapi
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["openapi"] = "3.0.2"
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(admin_auth.router, prefix="/api/admin-auth", tags=["后台认证"])
app.include_router(users.router, prefix="/api/users", tags=["用户"])
app.include_router(products.router, prefix="/api/products", tags=["商品"])
app.include_router(orders.router, prefix="/api/orders", tags=["订单"])
app.include_router(addresses.router, prefix="/api/addresses", tags=["地址"])
app.include_router(payment.router, prefix="/api/payment", tags=["支付"])
app.include_router(upload.router, prefix="/api/upload", tags=["上传"])

# 静态文件服务
import os
if os.path.exists("uploads"):
    app.mount("/static", StaticFiles(directory="uploads"), name="static")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """自定义 Swagger UI，使用国内 CDN"""
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        swagger_js_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.15.5/swagger-ui-bundle.min.js",
        swagger_css_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.15.5/swagger-ui.min.css",
    )


@app.get("/")
async def root():
    """健康检查"""
    return {"message": "网上订水 API 服务运行中", "version": "1.0.0"}


@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

