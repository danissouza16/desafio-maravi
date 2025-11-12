# import sys
# import os
# import json
# from unittest.mock import MagicMock, patch
# from datetime import time
# from app.worker.tasks import task_verificar_alertas
# from app.db.models import Alerta
# sys.path.append(os.getcwd())

# dados_onibus_fake = [
#     {"linha": "474", "latitude": -22.9068, "longitude": -43.1729, "velocidade": 50}
# ]

# alerta_fake = Alerta(
#     email_usuario="danielsantana2210@gmail.com",
#     linha_onibus="474",
#     ponto_partida_lat=-22.90,
#     ponto_partida_lon=-43.20,
#     horario_inicio=time(0,0), 
#     horario_fim=time(23,59),
#     notificacao_enviada=False
# )

# print("\n" + "="*50)
# print(">>> INICIANDO TESTE DE LÓGICA (COM MOCKS) <<<")
# print("="*50)

# with patch('app.services.cache_service.redis_client.get') as mock_redis:
#     mock_redis.return_value = json.dumps(dados_onibus_fake)
    
#     with patch('app.services.eta_service.get_estimated_travel_time', return_value=300):
#         with patch('app.services.email_service.send_notification_email') as mock_email:
#             with patch('app.worker.tasks.get_session_context') as mock_session_ctx:
#                 mock_session = MagicMock()
                
#                 mock_session.exec.return_value.all.return_value = [alerta_fake]
#                 mock_session_ctx.return_value.__enter__.return_value = mock_session
                
#                 print("1. Executando a tarefa 'task_verificar_alertas'...")
#                 try:
#                     retorno = task_verificar_alertas()
#                     print(f"   -> Tarefa finalizou sem erros. Retorno: {retorno}")
#                 except Exception as e:
#                     print(f"   -> ❌ ERRO CRÍTICO NA TAREFA: {e}")

#                 print("\n2. Verificando resultados:")
                
#                 if mock_email.called:
#                     print("   ✅ SUCESSO! A função de enviar e-mail FOI chamada!")
#                     args = mock_email.call_args[1] 
#                     print(f"      - Para: {args.get('email_to')}")
#                     print(f"      - Linha: {args.get('linha')}")
#                     print(f"      - Tempo Estimado: {args.get('tempo_estimado_min')} min")
#                 else:
#                     print("   ❌ FALHA: O código rodou, mas NÃO tentou enviar e-mail.")
#                     print("      (Verifique se a lógica do 'if eta <= 10' está correta)")

#                 if alerta_fake.notificacao_enviada is True:
#                      print("   ✅ SUCESSO! O alerta foi marcado como 'enviado' no objeto.")
#                 else:
#                      print("   ❌ FALHA: O alerta não foi atualizado para True.")

# print("="*50 + "\n")