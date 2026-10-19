from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.schemas import EventoSismicoCrear, EventoSismicoOut
from app.security import obtener_usuario_actual
from app.crud import eventos as crud_eventos

router = APIRouter(prefix="/api/eventos", tags=["Eventos"])


@router.post("", response_model=EventoSismicoOut, status_code=status.HTTP_201_CREATED)
def registrar(
    datos: EventoSismicoCrear,
    db: Session = Depends(get_db),
    usuario=Depends(obtener_usuario_actual),
):
    return crud_eventos.registrar_evento(db, usuario.id_usuario, datos)


@router.get("", response_model=List[EventoSismicoOut])
def listar(
    desde: Optional[datetime] = Query(None),
    hasta: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    usuario=Depends(obtener_usuario_actual),
):
    return crud_eventos.listar_eventos(db, usuario.id_usuario, desde, hasta)


@router.get("/{id_evento}", response_model=EventoSismicoOut)
def detalle(
    id_evento: int,
    db: Session = Depends(get_db),
    usuario=Depends(obtener_usuario_actual),
):
    return crud_eventos.obtener_evento(db, usuario.id_usuario, id_evento)
