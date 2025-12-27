"""短信验证码服务"""

import random
import time
from typing import Optional
from app.config import get_settings

settings = get_settings()

# 内存存储验证码（开发环境）
_verification_codes = {}


class SMSService:
    """短信服务类"""
    
    def __init__(self):
        self.environment = getattr(settings, 'environment', 'dev')
        self.code_expire_minutes = getattr(settings, 'code_expire_minutes', 5)
    
    def generate_code(self) -> str:
        """生成6位数字验证码"""
        return str(random.randint(100000, 999999))
    
    def send_code(self, phone: str) -> str:
        """发送验证码（5分钟内同一手机号返回相同验证码）"""
        current_time = time.time()
        
        # 检查是否已有未过期的验证码
        if phone in _verification_codes:
            stored = _verification_codes[phone]
            # 如果验证码未过期，返回相同的验证码
            if current_time < stored['expires_at']:
                print(f"[开发环境] 手机号 {phone} 的验证码: {stored['code']} (有效期剩余 {int((stored['expires_at'] - current_time) / 60)} 分钟)")
                return stored['code']
        
        # 生成新验证码
        code = self.generate_code()
        expires_at = current_time + (self.code_expire_minutes * 60)
        
        # 存储验证码
        _verification_codes[phone] = {
            'code': code,
            'expires_at': expires_at,
            'created_at': current_time
        }
        
        if self.environment == 'dev':
            # 开发环境：打印验证码
            print(f"[开发环境] 手机号 {phone} 的验证码: {code} (有效期 {self.code_expire_minutes} 分钟)")
        else:
            # 生产环境：调用短信服务商API
            # TODO: 集成实际的短信服务商（如阿里云、腾讯云等）
            # self._send_sms(phone, code)
            pass
        
        return code
    
    def verify_code(self, phone: str, code: str) -> bool:
        """验证验证码"""
        if phone not in _verification_codes:
            return False
        
        stored = _verification_codes[phone]
        
        # 检查是否过期
        if time.time() > stored['expires_at']:
            del _verification_codes[phone]
            return False
        
        # 检查验证码是否正确
        if stored['code'] != code:
            return False
        
        # 验证成功后删除验证码（一次性使用）
        del _verification_codes[phone]
        return True
    
    def _send_sms(self, phone: str, code: str):
        """发送短信（生产环境）"""
        # TODO: 实现实际的短信发送逻辑
        # 示例：使用阿里云短信服务
        # from aliyunsdkcore.client import AcsClient
        # from aliyunsdkcore.request import CommonRequest
        pass
    
    def get_code_for_testing(self, phone: str) -> Optional[str]:
        """获取验证码（仅用于测试）"""
        if self.environment == 'dev' and phone in _verification_codes:
            return _verification_codes[phone]['code']
        return None

