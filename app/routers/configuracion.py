from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.schemas import ConfiguracionSensibilidadIn, ConfiguracionSensibilidadOut
from app.security import obtener_usuario_actual
from app.crud import configuracion as crud_configuracion

router = APIRouter(prefix="/api/configuracion", tags=["Configuracion"])


@router.get("/sensibilidad", response_model=ConfiguracionSensibilidadOut)
def obtener(db: Session = Depends(get_db), usuario=Depends(obtener_usuario_actual)):
    return crud_configuracion.obtener_configuracion(db, usuario.id_usuario)


@router.put("/sensibilidad", response_model=ConfiguracionSensibilidadOut)
def actualizar(
    datos: ConfiguracionSensibilidadIn,
    db: Session = Depends(get_db),
    usuario=Depends(obtener_usuario_actual),
):
    return crud_configuracion.actualizar_configuracion(db, usuario.id_usuario, datos)
