"""应用配置：通过 pydantic-settings 从环境变量加载，类型安全。"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """全局配置。

    所有字段都可通过环境变量覆盖。例如:
        APP_NAME=foo  → settings.app_name == "foo"
    """

    model_config = SettingsConfigDict(
        env_file=".env",  # 自动读 .env
        env_file_encoding="utf-8",
        case_sensitive=False,  # 大小写不敏感
        extra="ignore",  # 忽略未声明的环境变量
    )

    # 基础
    app_name: str = Field(default="geetar-agent", description="应用名")
    app_env: str = Field(default="dev", description="运行环境: dev/prod")
    app_version: str = Field(default="0.1.0", description="版本号")

    # 服务器
    host: str = Field(default="0.0.0.0", description="监听地址")
    port: int = Field(default=8000, description="监听端口")


# 单例：全局共享
settings = Settings()
