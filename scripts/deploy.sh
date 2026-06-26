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

echo "==> 确保共享网络 web 存在"
docker network inspect web >/dev/null 2>&1 || docker network create web

echo "==> 构建并启动容器"
# 只用 base 文件，绝对不带 override（生产无热重载、不绑 host 端口）
docker compose -f docker-compose.yml build app
docker compose -f docker-compose.yml up -d --remove-orphans

echo "==> 等待健康检查（容器内访问，因为生产不绑 host 端口）"
healthy=0
for i in {1..30}; do
  if docker compose -f docker-compose.yml exec -T app \
       python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" \
       >/dev/null 2>&1; then
    echo "✓ App is healthy"
    healthy=1
    break
  fi
  sleep 2
done

if [[ $healthy -eq 0 ]]; then
  echo "✗ App did not become healthy in 60s. Recent logs:"
  docker compose -f docker-compose.yml logs --tail 50 app
  exit 1
fi

echo "==> 清理无用镜像"
docker image prune -f

echo "✓ Deploy done"
