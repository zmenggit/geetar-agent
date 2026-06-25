"""应用配置：通过 pydantic-settings 从环境变量加载，类型安全。"""

import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """全局配置。"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ─── 应用基础 ───
    app_name: str = Field(default="geetar-agent")
    app_env: str = Field(default="dev")
    app_version: str = Field(default="0.1.0")

    # ─── 服务器 ───
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)

    # ─── LLM 网关 ───
    llm_api_key: str = Field(default="")
    llm_base_url: str = Field(
        default="https://ark.cn-beijing.volces.com/api/coding/v3",
    )
    llm_model: str = Field(default="glm-5.2")
    llm_fast_model: str = Field(default="glm-5-flash")

    # ─── LangSmith ───
    langsmith_tracing: bool = Field(default=False)
    langsmith_api_key: str = Field(default="")
    langsmith_project: str = Field(default="geetar-agent-dev")
    langsmith_endpoint: str = Field(default="https://api.smith.langchain.com")


settings = Settings()


def _export_langsmith_env() -> None:
    """把 LangSmith 配置同步到 os.environ。

    LangChain 内部直接读 os.environ，不知道 pydantic-settings 的存在。
    没有这步，即使 .env 里 LANGSMITH_TRACING=true，trace 也不会上报。
    """
    if not settings.langsmith_tracing:
        return
    os.environ["LANGSMITH_TRACING"] = "true"
    os.environ["LANGSMITH_API_KEY"] = settings.langsmith_api_key
    os.environ["LANGSMITH_PROJECT"] = settings.langsmith_project
    os.environ["LANGSMITH_ENDPOINT"] = settings.langsmith_endpoint


_export_langsmith_env()
