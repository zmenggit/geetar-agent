"""LLM 客户端工厂：基于 OpenAI 兼容协议接入火山方舟编程套餐。"""

from functools import lru_cache
from typing import Literal

from langchain_openai import ChatOpenAI

from geetar_agent.config import settings

ModelTier = Literal["main", "fast"]


@lru_cache(maxsize=4)
def get_chat_model(tier: ModelTier = "main") -> ChatOpenAI:
    """返回一个 ChatOpenAI 实例（按 tier 缓存为单例）。

    Args:
        tier: "main" 主模型（复杂任务），"fast" 便宜快模型（路由/分类）
    """
    if not settings.llm_api_key:
        raise RuntimeError("LLM_API_KEY is not set. Please configure it in .env")

    model_name = {
        "main": settings.llm_model,
        "fast": settings.llm_fast_model,
    }[tier]

    return ChatOpenAI(
        model=model_name,
        api_key=settings.llm_api_key,
        base_url=settings.llm_base_url,
        temperature=0.7,
        timeout=30,
        max_retries=2,
    )
