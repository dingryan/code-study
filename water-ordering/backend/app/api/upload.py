"""文件上传相关 API"""

import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from pathlib import Path
from app.utils.response import success_response, error_response

router = APIRouter()

# 配置上传目录
UPLOAD_DIR = Path(__file__).parent.parent.parent / "static" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# 允许的文件类型
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def allowed_file(filename: str) -> bool:
    """检查文件扩展名是否允许"""
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


@router.post("/image")
async def upload_image(request: Request, file: UploadFile = File(...)):
    """上传图片"""
    try:
        # 检查文件类型
        if not allowed_file(file.filename):
            return error_response(
                code=400,
                message=f"不支持的文件类型。支持的格式: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # 读取文件内容
        contents = await file.read()
        file_size = len(contents)
        
        # 检查文件大小
        if file_size > MAX_FILE_SIZE:
            return error_response(
                code=400,
                message=f"文件太大。最大支持 {MAX_FILE_SIZE // (1024*1024)}MB"
            )
        
        # 生成唯一文件名
        file_extension = Path(file.filename).suffix.lower()
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = UPLOAD_DIR / unique_filename
        
        # 保存文件
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # 获取完整URL
        base_url = str(request.base_url).rstrip('/')
        file_url = f"{base_url}/static/uploads/{unique_filename}"
        
        return success_response(
            data={"url": file_url, "filename": unique_filename},
            message="上传成功"
        )
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return error_response(code=500, message=f"上传失败: {str(e)}")


@router.delete("/image/{filename}")
async def delete_image(filename: str):
    """删除图片"""
    try:
        file_path = UPLOAD_DIR / filename
        
        if not file_path.exists():
            return error_response(code=404, message="文件不存在")
        
        # 删除文件
        os.remove(file_path)
        
        return success_response(data=None, message="删除成功")
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return error_response(code=500, message=f"删除失败: {str(e)}")
