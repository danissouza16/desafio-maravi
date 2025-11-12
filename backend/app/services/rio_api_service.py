import requests
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

def fetch_bus_data_from_rio_api():
    """
    Busca dados de todos os ônibus na API da Prefeitura.
    INCLUI DADOS FALSOS (MOCK) PARA TESTE.
    """
    url = "[https://dados.mobilidade.rio/gps/sppo](https://dados.mobilidade.rio/gps/sppo)"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        #Se a API não retornar uma lista válida de veículos, usamos dados falsos
        if not isinstance(data, list) or len(data) == 0:
            logger.warning("SERVIÇO: API do Rio vazia. Usando DADOS DE TESTE (MOCK).")
            return [
                {
                    "ordem": "TESTE-01",
                    "linha": "474",
                    "latitude": -22.9029,  
                    "longitude": -43.1990, 
                    "velocidade": 40,
                    "datahora": "2025-11-12 12:00:00" 
                }
            ]
            
        #Se a API funcionou, retorna os dados reais
        logger.info(f"SERVIÇO: API do Rio retornou {len(data)} ônibus.")
        return data
        
    except Exception as e:
        logger.warning(f"SERVIÇO: Erro na API. Usando DADOS DE TESTE (MOCK). Erro: {e}")
        #Retorna o mesmo dado falso em caso de erro
        return [
            {
                "ordem": "TESTE-01",
                "linha": "474",
                "latitude": -22.9029,  
                "longitude": -43.1990, 
                "velocidade": 40,
                "datahora": "2025-11-12 12:00:00"
            }
        ]