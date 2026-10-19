from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.schemas import ContactoEmergenciaIn, ContactoEmergenciaOut
from app.security import obtener_usuario_actual
from app.crud import contactos as crud_contactos

router = APIRouter(prefix="/api/contactos-emergencia", tags=["Contactos de emergencia"])


@router.get("", response_model=List[ContactoEmergenciaOut])
def listar(db: Session = Depends(get_db), usuario=Depends(obtener_usuario_actual)):
    return crud_contactos.listar_contactos(db, usuario.id_usuario)


@router.post("", response_model=ContactoEmergenciaOut, status_code=status.HTTP_201_CREATED)
def crear(
    datos: ContactoEmergenciaIn,
    db: Session = Depends(get_db),
    usuario=Depends(obtener_usuario_actual),
):
    return crud_contactos.crear_contacto(db, usuario.id_usuario, datos)


@router.delete("/{id_contacto}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(
    id_contacto: int,
    db: Session = Depends(get_db),
    usuario=Depends(obtener_usuario_actual),
):
    crud_contactos.eliminar_contacto(db, usuario.id_usuario, id_contacto)
