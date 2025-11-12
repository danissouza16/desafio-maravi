Desafio Maravi - Alerta de Ônibus

Este projeto é uma solução completa para o desafio de processo seletivo da Maravi, implementando um sistema de monitoramento e alerta de ônibus em tempo real para a cidade do Rio de Janeiro.

O aplicativo permite que usuários cadastrem alertas para linhas de ônibus específicas e sejam notificados por e-mail quando um veículo estiver a 10 minutos de seu ponto de partida. Além disso, fornece um dashboard para visualização em tempo real da frota em um mapa e tabela.

Funcionalidades

API Backend (FastAPI):

Criação de Alertas (POST /api/v1/alertas/).

Endpoint de dados em tempo real para o dashboard (GET /api/v1/onibus/{linha}).

Validação de dados com Pydantic.

Comunicação com banco de dados (PostgreSQL com SQLModel).

Serviços de Worker (Celery):

Coletor de Dados: Uma tarefa (task_buscar_dados_onibus) que roda a cada minuto, busca dados da API dados.mobilidade.rio e os salva no cache (Redis).

Processador de Alertas: Uma tarefa (task_verificar_alertas) que roda a cada minuto, verifica alertas ativos, busca ônibus no cache e calcula o tempo de chegada (ETA).

Cálculo de ETA (TravelTime):

Utiliza a API da TravelTime para calcular o tempo de viagem real (em segundos) entre a posição atual do ônibus e o ponto de partida do usuário.

Notificações (SendGrid):

Envia um e-mail formatado para o usuário via SendGrid se um ônibus estiver a 10 minutos ou menos.

Frontend (React):

Página de Alerta: Formulário para cadastro de novos alertas com validação de campos.

Página de Dashboard:

Campo de busca para filtrar por linha de ônibus.

Mapa (Leaflet): Exibe a posição de todos os ônibus da linha selecionada em tempo real.

Tabela: Lista os detalhes dos veículos (placa, velocidade, etc.).

Infraestrutura (Docker):

100% Dockerizado: O projeto é orquestrado com docker-compose.

6 Containers: backend (FastAPI), frontend (React), worker (Celery), beat (Celery Scheduler), db (Postgres) e redis (Cache/Broker).

Stack Tecnológica

Backend: Python 3.11, FastAPI, SQLModel, Celery

Frontend: React.js, Axios, Leaflet, react-leaflet

Banco de Dados: PostgreSQL

Cache/Message Broker: Redis

Infraestrutura: Docker & Docker Compose

APIs Externas: SendGrid (E-mail), TravelTime (ETA), Dados.Rio (GPS)

Como Executar o Projeto

Certifique-se de que o Docker Desktop esteja instalado e rodando na sua máquina.

1. Configuração de Variáveis de Ambiente

O projeto requer chaves de API para funcionar.

Crie o arquivo .env.backend na raiz do projeto (ao lado do docker-compose.yml) e preencha com suas chaves:

# .env.backend

# Chave de API do SendGrid (para enviar e-mails)
SENDGRID_API_KEY=SUA_CHAVE_AQUI
SENDGRID_FROM_EMAIL=seu-email-verificado-no-sendgrid@gmail.com

# Chaves da API TravelTime (para calcular o tempo)
TRAVELTIME_APP_ID=SEU_APP_ID_AQUI
TRAVELTIME_API_KEY=SUA_CHAVE_AQUI


Crie o arquivo .env.db na raiz do projeto (ao lado do docker-compose.yml) para configurar o banco:

# .env.db

POSTGRES_DB=maravi_bus_db
POSTGRES_USER=maravi_user
POSTGRES_PASSWORD=maravi_secret_password


2. Subindo os Containers

Com os arquivos .env criados, execute o seguinte comando na raiz do projeto:

docker compose up --build


O Docker irá baixar as imagens, construir os containers e iniciar todos os 6 serviços. Isso pode levar alguns minutos na primeira vez.

3. Acessando a Aplicação

Após os containers subirem:

Aplicação Frontend (React):

Abra no navegador: http://localhost:3000

Documentação da API (FastAPI):

Abra no navegador: http://localhost:8000/docs

Prints da Aplicação

![alt text](image-2.png)


![alt text](image-1.png)


![alt text](image-3.png)