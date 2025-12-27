"""文件上传相关 API"""

import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
from app.models.admin_user import AdminUser
from app.utils.dependencies import get_admin_user
from app.utils.response import success_response, error_response
from app.config import get_settings

settings = get_settings()
router = APIRouter()

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
    current_admin: AdminUser = Depends(get_admin_user)
):
    """上传图片（管理员权限）"""
    try:
        if not file.content_type or not file.content_type.startswith('image/'):
            return error_response(code=400, message="只能上传图片文件")
        
        file_ext = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
        file_name = f"{uuid.uuid4().hex}.{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, file_name)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        image_url = f"http://localhost:8000/static/{file_name}"
        return success_response(data={"url": image_url}, message="上传成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        return error_response(code=500, message=f"上传失败: {str(e)}")

