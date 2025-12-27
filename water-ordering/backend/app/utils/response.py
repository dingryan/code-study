"""统一响应格式"""

import uuid
from typing import Any
from fastapi.responses import JSONResponse


def success_response(data: Any = None, message: str = "操作成功.") -> JSONResponse:
    """成功响应"""
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
    """错误响应"""
    return JSONResponse(
        status_code=200,  # 统一返回200状态码
        content={
            "code": "0",
            "data": data if data is not None else {"error": message},
            "msg": message,
            "requestId": str(uuid.uuid4()).replace("-", "")
        }
    )

