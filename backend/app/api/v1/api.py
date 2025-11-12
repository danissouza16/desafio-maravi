from fastapi import APIRouter
from app.api.v1.endpoints import alertas, onibus

api_router = APIRouter()

api_router.include_router(
    alertas.router,
    prefix="/alertas",
    tags=["Alertas"]
)
api_router.include_router(
    onibus.router,
    prefix="/onibus",
    tags=["Ônibus"]
)