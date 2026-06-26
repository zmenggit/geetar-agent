#!/usr/bin/env bash
# 服务器端发版脚本：在 ~/geetar-agent 下执行 ./scripts/deploy.sh

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

echo "==> 拉取最新代码"
git fetch --all
git reset --hard origin/main

echo "==> 检查 .env"
if [[ ! -f .env ]]; then
  echo "✗ .env not found. Copy from .env.example and fill in secrets."
  exit 1
fi

echo "==> 构建并启动容器"
# 用 base 文件，绝对不带 override（生产无热重载）
docker compose -f docker-compose.yml build app
docker compose -f docker-compose.yml up -d --remove-orphans

echo "==> 等待健康检查"
for i in {1..30}; do
  if curl -fsS http://127.0.0.1:8000/health > /dev/null; then
    echo "✓ App is healthy"
    break
  fi
  sleep 2
done

echo "==> 清理无用镜像"
docker image prune -f

echo "✓ Deploy done"