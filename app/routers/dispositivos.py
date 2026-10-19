from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.schemas import DispositivoCrear, DispositivoOut, CalibracionOut
from app.security import obtener_usuario_actual
from app.crud import dispositivos as crud_dispositivos

router = APIRouter(prefix="/api/dispositivos", tags=["Dispositivos"])


@router.post("", response_model=DispositivoOut, status_code=status.HTTP_201_CREATED)
def registrar(
    datos: DispositivoCrear,
    db: Session = Depends(get_db),
    usuario=Depends(obtener_usuario_actual),
):
    return crud_dispositivos.registrar_dispositivo(db, usuario.id_usuario, datos)


@router.get("/{id_dispositivo}/calibracion", response_model=CalibracionOut)
def calibracion(id_dispositivo: int, db: Session = Depends(get_db)):
    return crud_dispositivos.obtener_calibracion(db, id_dispositivo)
