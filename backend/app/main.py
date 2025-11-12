from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.db.base import create_db_and_tables
from app.api.v1.api import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Inicializando aplicação...")
    create_db_and_tables()
    print("Tabelas criadas")
    yield
    print("Encerrando a aplicação...")

app = FastAPI(
    title="Maravi Alerta de Onibus",
    description="API para desafio Maravi",
    version="1.0.0",
    lifespan=lifespan
)

origins = [
    "http://localhost",
    "http://localhost:3000", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["Health Check"])
def read_root():
    return {"status": "ok", 'message': "API is running"}