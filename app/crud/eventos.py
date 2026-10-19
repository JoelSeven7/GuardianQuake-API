from typing import Optional
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.models import EventoSismico
from app.schemas.schemas import EventoSismicoCrear


def registrar_evento(db: Session, id_usuario: int, datos: EventoSismicoCrear) -> EventoSismico:
    evento = EventoSismico(
        id_usuario=id_usuario,
        id_dispositivo=datos.id_dispositivo,
        fecha_hora=datos.fecha_hora,
        intensidad_aproximada=datos.intensidad_aproximada,
        duracion_ms=datos.duracion_ms,
        sensibilidad_usada=datos.sensibilidad_usada,
    )
    db.add(evento)
    db.commit()
    db.refresh(evento)
    return evento


def listar_eventos(
    db: Session, id_usuario: int, desde: Optional[datetime] = None, hasta: Optional[datetime] = None
):
    query = db.query(EventoSismico).filter(EventoSismico.id_usuario == id_usuario)
    if desde:
        query = query.filter(EventoSismico.fecha_hora >= desde)
    if hasta:
        query = query.filter(EventoSismico.fecha_hora <= hasta)
    return query.order_by(EventoSismico.fecha_hora.desc()).all()


def obtener_evento(db: Session, id_usuario: int, id_evento: int) -> EventoSismico:
    evento = db.query(EventoSismico).filter(
        EventoSismico.id_evento == id_evento, EventoSismico.id_usuario == id_usuario
    ).first()
    if not evento:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Evento no encontrado")
    return evento
