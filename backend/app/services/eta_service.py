import requests
import logging
from datetime import datetime
from app.core.config import settings

logger = logging.getLogger(__name__)

def get_estimated_travel_time(origem_lat: float, origem_lon: float, destino_lat: float, destino_lon: float):
    
    url = "https://api.traveltimeapp.com/v4/time-filter"
    
    #Horário de partida (em formato UTC)
    departure_time_utc = datetime.utcnow().isoformat() + "Z"
    
    #Payload format
    payload = {
        "locations": [
            {
                "id": "ponto_destino",
                "coords": {"lat": destino_lat, "lng": destino_lon}
            },
            {
                "id": "onibus_origem",
                "coords": {"lat": origem_lat, "lng": origem_lon}
            }
        ],
        "departure_searches": [
            {
                "id": "calculo_eta_onibus",
                "departure_location_id": "onibus_origem",
                "arrival_location_ids": ["ponto_destino"],
                "transportation": {"type": "driving"}, 
                "departure_time": departure_time_utc,
                "travel_time": 3600, 
                "properties": ["travel_time"]
            }
        ]
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Application-Id": settings.TRAVELTIME_APP_ID,
        "X-Api-Key": settings.TRAVELTIME_API_KEY
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  
        
        results = response.json().get('results', [])
        
        if not results or 'locations' not in results[0] or not results[0]['locations']:
            logger.warning("API TravelTime não retornou um ETA válido.")
            return float('inf') 

        #Retorna o tempo de viagem em segundos
        travel_time_sec = results[0]['locations'][0]['properties'][0]['travel_time']
        return travel_time_sec

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"Erro HTTP ao chamar API TravelTime: {http_err.response.status_code} {http_err.response.text}")
        raise
    except Exception as e:
        logger.error(f"Erro inesperado no serviço ETA: {e}")
        raise