"""聊天端点：调用 LLM 返回回答。"""

from fastapi import APIRouter, HTTPException
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

from geetar_agent.llm.client import get_chat_model

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    """聊天请求。"""

    message: str = Field(..., min_length=1, max_length=2000, description="用户消息")
    system: str | None = Field(
        default=None,
        max_length=2000,
        description="可选 system prompt，覆盖默认人设",
    )


class ChatResponse(BaseModel):
    """聊天响应。"""

    reply: str = Field(..., description="LLM 回答")
    model: str = Field(..., description="使用的模型名")


DEFAULT_SYSTEM_PROMPT = (
    "你是一位资深吉他老师，对吉他演奏、乐理、和弦走向、谱面解读都很在行。回答要专业、简洁、亲切。"
)


@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    """单轮聊天：用户传一句话，返回 LLM 回答。"""
    model = get_chat_model()

    messages = [
        SystemMessage(content=req.system or DEFAULT_SYSTEM_PROMPT),
        HumanMessage(content=req.message),
    ]

    try:
        result = await model.ainvoke(messages)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM call failed: {e}") from e

    return ChatResponse(
        reply=str(result.content),
        model=model.model_name,
    )
