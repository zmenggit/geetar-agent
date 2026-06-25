from fastapi import FastAPI

from geetar_agent.api import chat, health
from geetar_agent.config import settings


def create_app() -> FastAPI:
    """应用工厂：返回一个配置好的 FastAPI 实例。

    用工厂函数而不是模块级单例的好处：
    - 测试时可以多次创建独立实例
    - 便于后期扩展（DI、生命周期管理等）
    """
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="吉他领域 AI Agent",
    )

    # 注册路由
    app.include_router(health.router)
    app.include_router(chat.router)

    return app


app = create_app()
