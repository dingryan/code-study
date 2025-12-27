"""配置管理模块"""

import os
import yaml
from pydantic_settings import BaseSettings
from typing import List


def load_yaml_config():
    """从 YAML 文件加载配置"""
    cur_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(cur_path, "..", "config", "config.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.load(f.read(), Loader=yaml.FullLoader)


class Settings(BaseSettings):
    """应用配置"""
    
    app_name: str = "网上订水 API"
    debug: bool = False
    environment: str = "dev"  # dev 或 prod
    database_url: str = ""
    secret_key: str = ""
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    cors_origins: List[str] = ["*"]
    code_expire_minutes: int = 5  # 验证码有效期（分钟）
    wechat_app_id: str = ""
    wechat_app_secret: str = ""
    wechat_mch_id: str = ""
    wechat_api_key: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = False


_settings = None


def get_settings() -> Settings:
    """获取配置实例（单例模式）"""
    global _settings
    if _settings is None:
        yaml_config = load_yaml_config()
        _settings = Settings(**yaml_config)
    return _settings

