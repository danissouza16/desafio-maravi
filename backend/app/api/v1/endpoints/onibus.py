from fastapi import APIRouter, HTTPException
from app.services import cache_service

router = APIRouter()

@router.get("/{linha}")
def get_onibus_por_linha(linha: str):
    dados = cache_service.get_bus_data_from_cache(linha)
    
    if not dados:
        return {"linha": linha, "total": 0, "veiculos": []}
    
    return {
        "linha": linha,
        "total": len(dados),
        "veiculos": dados
    }