from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.schemas import VerificarCompraIn, SuscripcionOut, EstadoSuscripcionOut
from app.security import obtener_usuario_actual
from app.crud import suscripcion as crud_suscripcion

router = APIRouter(prefix="/api/suscripcion", tags=["Suscripcion"])


@router.get("/estado", response_model=EstadoSuscripcionOut)
def estado(db: Session = Depends(get_db), usuario=Depends(obtener_usuario_actual)):
    return crud_suscripcion.obtener_estado(db, usuario)


@router.post("/verificar-compra", response_model=SuscripcionOut, status_code=status.HTTP_201_CREATED)
def verificar_compra(
    datos: VerificarCompraIn,
    db: Session = Depends(get_db),
    usuario=Depends(obtener_usuario_actual),
):
    return crud_suscripcion.verificar_compra(db, usuario, datos)


@router.post("/cancelar", response_model=SuscripcionOut)
def cancelar(db: Session = Depends(get_db), usuario=Depends(obtener_usuario_actual)):
    return crud_suscripcion.cancelar_suscripcion(db, usuario)
