"""统一响应格式和错误处理装饰器"""

import uuid
import traceback
from typing import Any, Callable
from functools import wraps
from fastapi.responses import JSONResponse


def success_response(data: Any = None, message: str = "操作成功.") -> JSONResponse:
    """统一成功响应格式"""
    return JSONResponse(
        status_code=200,
        content={
            "code": "0",
            "data": data,
            "msg": message,
            "requestId": str(uuid.uuid4()).replace("-", "")
        }
    )


def error_response(code: int = 400, message: str = "操作失败", data: Any = None) -> JSONResponse:
    """统一错误响应格式"""
    return JSONResponse(
        status_code=200,
        content={
            "code": "0",
            "data": data if data is not None else {"error": message},
            "msg": message,
            "requestId": str(uuid.uuid4()).replace("-", "")
        }
    )


def handle_errors(func: Callable) -> Callable:
    """统一错误处理装饰器"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            traceback.print_exc()
            return error_response(code=500, message=str(e))
    return wrapper
