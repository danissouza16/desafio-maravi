from pydantic_settings import BaseSettings
from pydantic import EmailStr

class Settings(BaseSettings):
    #variáveis carregadas automaticamente do ambiente (ou do .env.backend)
    DATABASE_URL: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    
    #Chaves para a API de cálculo de tempo
    TRAVELTIME_API_KEY: str
    TRAVELTIME_APP_ID: str

    # onfigurações de E-mail
    SENDGRID_API_KEY: str
    EMAIL_FROM: EmailStr = "daniel.santana2210@gmail.com"
    
#Instância única das configurações que será usada em todo o app
settings = Settings()