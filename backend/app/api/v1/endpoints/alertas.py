from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.db.base import get_session
from app.db.models import Alerta
from app.schemas.alerta import AlertaCreate, AlertaRead, AlertaUpdate

router = APIRouter()

@router.post(
    "/", 
    response_model=AlertaRead,
    status_code=status.HTTP_201_CREATED
)
def create_alerta(
    *,
    session: Session = Depends(get_session),
    alerta_in: AlertaCreate
):
    alerta_db = Alerta.model_validate(alerta_in)
    session.add(alerta_db)
    session.commit()
    session.refresh(alerta_db)
    return alerta_db

@router.get(
    "/",
    response_model=list[AlertaRead]
)
def read_alertas(
    *,
    session: Session = Depends(get_session),
):
    statement = select(Alerta)
    alertas = session.exec(statement).all()
    return alertas   