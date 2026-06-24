"""测试 /health 端点。"""

from fastapi.testclient import TestClient

from geetar_agent.main import create_app


def test_health_returns_ok() -> None:
    """健康检查应返回 200 和正确字段。"""
    app = create_app()
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["app"] == "geetar-agent"
    assert "version" in body
    assert "env" in body


def test_health_response_schema() -> None:
    """响应字段类型应正确。"""
    app = create_app()
    client = TestClient(app)

    body = client.get("/health").json()

    assert isinstance(body["status"], str)
    assert isinstance(body["app"], str)
