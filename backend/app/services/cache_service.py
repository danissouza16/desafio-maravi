import redis
import json
from app.core.config import settings

#Cria uma conexão com o Redis (o mesmo usado pelo Celery)
redis_client = redis.Redis.from_url(settings.CELERY_RESULT_BACKEND, decode_responses=True)

def save_bus_data_to_cache(bus_data: list[dict]):
    print(f"SERVIÇO: Salvando {len(bus_data)} registros de ônibus no cache Redis...")
    pipe = redis_client.pipeline()
    
    linhas_agrupadas = {}
    for onibus in bus_data:
        linha = onibus.get("linha") 
        if not linha:
            continue 

        if linha not in linhas_agrupadas:
            linhas_agrupadas[linha] = []
        linhas_agrupadas[linha].append(onibus)

    for linha, dados in linhas_agrupadas.items():
        pipe.set(f"onibus:{linha}", json.dumps(dados), ex=300) 
    
    pipe.execute()
    print("SERVIÇO: Dados salvos no Redis.")

def get_bus_data_from_cache(linha: str):
    key = f"onibus:{linha}"
    data_json = redis_client.get(key)
    
    if data_json:
        return json.loads(data_json)
    
    return []