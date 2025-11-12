from datetime import time
from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import ConfigDict

class AlertaBase(SQLModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    email_usuario: str = Field(index=True)
    linha_onibus: str = Field(index=True)

    ponto_partida_lat: float
    ponto_partida_lon: float

    horario_inicio: time
    horario_fim: time

class Alerta(AlertaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    notificacao_enviada: bool = Field(default=False)