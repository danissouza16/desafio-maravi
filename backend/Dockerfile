FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia apenas o arquivo de requisitos primeiro.
COPY requirements.txt requirements.txt

# Instala as dependências Python
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

#copia o resto do código-fonte da sua aplicação
COPY ./app /app/app

# Expõe a porta 8000 (onde o FastAPI/Uvicorn vai rodar)
EXPOSE 8000

# O 'command:' no docker-compose.yml vai sobrescrever este CMD.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]