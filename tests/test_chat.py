"""测试 /chat 端点（不调真实 LLM，用 mock）。"""

from unittest.mock import patch

from fastapi.testclient import TestClient
from langchain_core.messages import AIMessage

from geetar_agent.main import create_app


def test_chat_validation_rejects_empty_message() -> None:
    """空 message 应该被 Pydantic 拒绝，返回 422。"""
    app = create_app()
    client = TestClient(app)

    response = client.post("/chat", json={"message": ""})

    assert response.status_code == 422


def test_chat_validation_rejects_oversized_message() -> None:
    """超长 message 应被拒绝。"""
    app = create_app()
    client = TestClient(app)

    response = client.post("/chat", json={"message": "a" * 3000})

    assert response.status_code == 422


def test_chat_returns_reply_with_mocked_llm() -> None:
    """mock 掉 LLM 调用，验证端到端路径。"""
    fake_response = AIMessage(content="练习 F 和弦的几个建议...")

    with patch("geetar_agent.api.chat.get_chat_model") as mock_factory:
        mock_factory.return_value.ainvoke = _async_return(fake_response)
        mock_factory.return_value.model_name = "glm-5.2"

        app = create_app()
        client = TestClient(app)

        response = client.post("/chat", json={"message": "F 怎么练"})

    assert response.status_code == 200
    body = response.json()
    assert body["reply"] == "练习 F 和弦的几个建议..."
    assert body["model"] == "glm-5.2"


def _async_return(value):  # type: ignore[no-untyped-def]
    """构造一个返回固定值的 async mock。"""

    async def _coro(*args, **kwargs):
        return value

    return _coro
