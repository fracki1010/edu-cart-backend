# app/routers/health.py
from fastapi import APIRouter

# 1) Creo el enrutador
health_router = APIRouter()

# 2) Uso health_router en lugar de "router"
@health_router.get("/")
def health():
    return {"status": "ok"}

