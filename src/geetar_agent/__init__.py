
def main() -> None:
    """启动 web 服务。"""
    import uvicorn

    from geetar_agent.config import settings

    uvicorn.run(
        "geetar_agent.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.app_env == "dev",  # 开发环境自动热重载
    )
