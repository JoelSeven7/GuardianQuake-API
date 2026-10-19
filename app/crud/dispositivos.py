from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.models import Dispositivo
from app.schemas.schemas import DispositivoCrear


def registrar_dispositivo(db: Session, id_usuario: int, datos: DispositivoCrear) -> Dispositivo:
    dispositivo = Dispositivo(
        id_usuario=id_usuario,
        modelo=datos.modelo,
        fabricante=datos.fabricante,
        so_version=datos.so_version,
    )
    db.add(dispositivo)
    db.commit()
    db.refresh(dispositivo)
    return dispositivo


def obtener_calibracion(db: Session, id_dispositivo: int) -> Dispositivo:
    dispositivo = db.query(Dispositivo).filter(Dispositivo.id_dispositivo == id_dispositivo).first()
    if not dispositivo:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Dispositivo no encontrado")
    return dispositivo
