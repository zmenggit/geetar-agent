# syntax=docker/dockerfile:1.7

# ──────────────────────────────────────────────────────────────────
# Stage 1: Builder — 装依赖、构建虚拟环境
# ──────────────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

# 从官方 uv 镜像直接拷贝 uv 二进制（极快）
COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /uvx /bin/

# uv 行为微调
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/app/.venv \
    UV_HTTP_TIMEOUT=120 \
    UV_DEFAULT_INDEX=https://pypi.tuna.tsinghua.edu.cn/simple

WORKDIR /app

# ── 关键优化：依赖装到独立 layer，让 Docker 缓存 ──
# 只 copy 依赖描述文件，不 copy 源码
COPY pyproject.toml uv.lock ./

# 装依赖（不装项目本身、不装 dev 组、frozen 强制按 lockfile）
# cache mount 让多次构建复用 uv 缓存
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# 现在 copy 源码
COPY src ./src
COPY README.md ./

# 装项目自身（editable 模式，让 src layout 生效）
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# ──────────────────────────────────────────────────────────────────
# Stage 2: Runtime — 极简运行时
# ──────────────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

# 创建非 root 用户（生产安全实践）
RUN groupadd --system app && useradd --system --gid app --home /app app

WORKDIR /app

# 从 builder 阶段拷贝虚拟环境和源码
COPY --from=builder --chown=app:app /app/.venv /app/.venv
COPY --from=builder --chown=app:app /app/src /app/src

# 把 .venv 的 bin 加到 PATH，这样 uvicorn / geetar-agent 命令直接可用
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER app

EXPOSE 8000

# 健康检查（compose 也会用到）
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "geetar_agent.main:app", "--host", "0.0.0.0", "--port", "8000"]