from datetime import time
from typing import Optional
from sqlmodel import SQLModel
from pydantic import EmailStr

class AlertaBaseSchema(SQLModel):
    email_usuario: EmailStr
    linha_onibus: str
    ponto_partida_lat: float
    ponto_partida_lon: float
    horario_inicio: time
    horario_fim: time

class AlertaCreate(AlertaBaseSchema):
    pass

class AlertaRead(AlertaBaseSchema):
    id: int
    notificacao_enviada: bool

class AlertaUpdate(SQLModel):
    email_usuario: Optional[EmailStr] = None
    linha_onibus: Optional[str] = None
    ponto_partida_lat: Optional[float] = None
    ponto_partida_lon: Optional[float] = None
    horario_inicio: Optional[time] = None
    horario_fim: Optional[time] = None
    notificacao_enviada: Optional[bool] = None