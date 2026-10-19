from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.models import ContenidoEducativo


def listar_contenido(db: Session):
    return db.query(ContenidoEducativo).order_by(ContenidoEducativo.fecha_publicacion.desc()).all()


def obtener_contenido(db: Session, id_contenido: int) -> ContenidoEducativo:
    contenido = db.query(ContenidoEducativo).filter(
        ContenidoEducativo.id_contenido == id_contenido
    ).first()
    if not contenido:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Contenido no encontrado")
    return contenido
