from sqlalchemy.orm import Session

from app.models.models import ConfiguracionSensibilidad
from app.schemas.schemas import ConfiguracionSensibilidadIn


def obtener_configuracion(db: Session, id_usuario: int) -> ConfiguracionSensibilidad:
    config = db.query(ConfiguracionSensibilidad).filter(
        ConfiguracionSensibilidad.id_usuario == id_usuario
    ).first()
    if not config:
        config = ConfiguracionSensibilidad(id_usuario=id_usuario, nivel=5)
        db.add(config)
        db.commit()
        db.refresh(config)
    return config


def actualizar_configuracion(
    db: Session, id_usuario: int, datos: ConfiguracionSensibilidadIn
) -> ConfiguracionSensibilidad:
    config = obtener_configuracion(db, id_usuario)
    config.nivel = datos.nivel
    db.commit()
    db.refresh(config)
    return config
