import logging
from datetime import datetime
from sqlmodel import select

from app.worker.celery_app import celery_app
from app.db.base import get_session_context
from app.db.models import Alerta
from app.services import (
    rio_api_service,
    cache_service,
    eta_service,
    email_service
)

logger = logging.getLogger(__name__)


@celery_app.task(name="app.worker.tasks.task_buscar_dados_onibus")
def task_buscar_dados_onibus():
    logger.info("CELERY TASK: Executando 'task_buscar_dados_onibus'...")
    dados_onibus = []
    try:
        # Busca dados da API 
        dados_onibus = rio_api_service.fetch_bus_data_from_rio_api()
        
        if not dados_onibus:
            logger.warning("API do Rio não retornou dados.")
            return "Nenhum ônibus encontrado."

        #Salva no cache Redis
        cache_service.save_bus_data_to_cache(dados_onibus)
        logger.warning(f"CELERY TASK: 'task_buscar_dados_onibus' concluída.")
        return f"{len(dados_onibus)} ônibus processados."
        
    except Exception as e:
        logger.error(f"Erro em 'task_buscar_dados_onibus': {e}")
        return f"Erro ao processar ônibus: {e}"


@celery_app.task(name="app.worker.tasks.task_verificar_alertas")
def task_verificar_alertas():
    logger.info("CELERY TASK: Executando 'task_verificar_alertas'...")
    alertas_processados = 0
    try:
        with get_session_context() as session:
            agora = datetime.now().time()
            
            #Busca todos os alertas ativos e não enviados
            statement = select(Alerta).where(
                Alerta.notificacao_enviada == False,
                Alerta.horario_inicio <= agora,
                Alerta.horario_fim >= agora
            )
            alertas = session.exec(statement).all()

            if not alertas:
                logger.warning("CELERY TASK: Nenhum alerta ativo na janela de horário.")
                return "Nenhum alerta ativo."

            alertas_processados = len(alertas)
            logger.warning(f"CELERY TASK: {alertas_processados} alertas ativos encontrados.")

            for alerta in alertas:
                #Busca dados do ônibus no cache (usando a função de serviço)
                dados_onibus_linha = cache_service.get_bus_data_from_cache(alerta.linha_onibus)
                
                if not dados_onibus_linha:
                    logger.warning(f"CELERY TASK: Sem dados no cache para a linha {alerta.linha_onibus}.")
                    continue 

                # --- TESTE---
                # Adiciona um ônibus falso
                dados_onibus_linha.append({
                    "ordem": "TESTE-GARANTIDO",
                    "latitude": -22.9029, 
                    "longitude": -43.1990,
                    "velocidade": 40
                })

                onibus_mais_proximo_eta = float('inf') # Infinito

                for onibus in dados_onibus_linha:
                    try:
                        if not onibus.get('latitude') or not onibus.get('longitude'):
                            logger.warning(f"Ônibus {onibus.get('ordem')} com coordenadas nulas. Pulando.")
                            continue
                            
                        if onibus.get('velocidade', 0) == 0:
                            continue

                        eta_segundos = eta_service.get_estimated_travel_time(
                            origem_lat=onibus['latitude'],
                            origem_lon=onibus['longitude'],
                            destino_lat=alerta.ponto_partida_lat,
                            destino_lon=alerta.ponto_partida_lon
                        )
                        
                        if eta_segundos < onibus_mais_proximo_eta:
                            onibus_mais_proximo_eta = eta_segundos
                            
                    except Exception as e:
                        logger.error(f"Erro ao calcular ETA para o ônibus {onibus.get('ordem')}: {e}")
                
                if onibus_mais_proximo_eta == float('inf'):
                    logger.warning(f"CELERY TASK: Nenhum ônibus em movimento ou com ETA calculável para a linha {alerta.linha_onibus}.")
                    continue 

                #Verificação se deve notificar
                eta_minutos = onibus_mais_proximo_eta / 60
                logger.info(f"CELERY TASK: Linha {alerta.linha_onibus}. ETA mais próximo: {eta_minutos:.1f} min.")
                
                #comentado para forçar o envio do e-mail
                # if eta_minutos <= 10: 
                
                logger.warning(f"!!! ALERTA ATIVADO (TESTE FORÇADO) !!! Linha {alerta.linha_onibus} a {eta_minutos:.1f} min do ponto.")
                print("------------------------------------------------------")
                print(f"SERVIÇO: *** ENVIANDO E-MAIL REAL (SendGrid) ***")
                print(f"PARA: {alerta.email_usuario}")
                print("------------------------------------------------------")
                
                #Envia o e-mail
                email_service.send_notification_email(
                    email_to=alerta.email_usuario,
                    linha=alerta.linha_onibus,
                    tempo_estimado_min=int(eta_minutos) 
                )
                
                #Marca o alerta como enviado no banco
                alerta.notificacao_enviada = True
                session.add(alerta)
                
    except Exception as e:
        logger.error(f"Erro inesperado na task 'task_verificar_alertas': {e}")
        session.rollback() 
    
    logger.warning("CELERY TASK: 'task_verificar_alertas' concluída.")
    return f"{alertas_processados} alertas processados."