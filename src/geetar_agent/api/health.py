from fastapi import APIRouter
from pydantic import BaseModel

from geetar_agent.config import settings

router = APIRouter(tags=["system"])

class HealthResponse(BaseModel):
  status: str
  app: str
  version: str
  env: str

@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
  return HealthResponse(
    status="ok",
    app=settings.app_name,
    version=settings.app_version,
    env=settings.app_env
  )