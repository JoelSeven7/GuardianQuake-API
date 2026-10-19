from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.models import ContactoEmergencia
from app.schemas.schemas import ContactoEmergenciaIn


def listar_contactos(db: Session, id_usuario: int):
    return db.query(ContactoEmergencia).filter(ContactoEmergencia.id_usuario == id_usuario).all()


def crear_contacto(db: Session, id_usuario: int, datos: ContactoEmergenciaIn) -> ContactoEmergencia:
    contacto = ContactoEmergencia(id_usuario=id_usuario, nombre=datos.nombre, telefono=datos.telefono)
    db.add(contacto)
    db.commit()
    db.refresh(contacto)
    return contacto


def eliminar_contacto(db: Session, id_usuario: int, id_contacto: int) -> None:
    contacto = db.query(ContactoEmergencia).filter(
        ContactoEmergencia.id_contacto == id_contacto, ContactoEmergencia.id_usuario == id_usuario
    ).first()
    if not contacto:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Contacto no encontrado")
    db.delete(contacto)
    db.commit()
