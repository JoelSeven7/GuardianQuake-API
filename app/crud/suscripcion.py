from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.models import Usuario, Suscripcion
from app.schemas.schemas import VerificarCompraIn


def obtener_estado(db: Session, usuario: Usuario) -> dict:
    suscripcion = db.query(Suscripcion).filter(
        Suscripcion.id_usuario == usuario.id_usuario, Suscripcion.estado == "ACTIVA"
    ).order_by(Suscripcion.fecha_inicio.desc()).first()
    return {"tipo_cuenta": usuario.tipo_cuenta, "suscripcion": suscripcion}


def verificar_compra(db: Session, usuario: Usuario, datos: VerificarCompraIn) -> Suscripcion:
    existente = db.query(Suscripcion).filter(
        Suscripcion.id_transaccion == datos.id_transaccion
    ).first()
    if existente:
        raise HTTPException(status.HTTP_409_CONFLICT, "Esta transaccion ya fue registrada")

    suscripcion = Suscripcion(
        id_usuario=usuario.id_usuario,
        id_transaccion=datos.id_transaccion,
        plataforma=datos.plataforma,
        estado="ACTIVA",
    )
    usuario.tipo_cuenta = "PRO"
    db.add(suscripcion)
    db.commit()
    db.refresh(suscripcion)
    return suscripcion


def cancelar_suscripcion(db: Session, usuario: Usuario) -> Suscripcion:
    suscripcion = db.query(Suscripcion).filter(
        Suscripcion.id_usuario == usuario.id_usuario, Suscripcion.estado == "ACTIVA"
    ).first()
    if not suscripcion:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No hay una suscripcion activa")

    suscripcion.estado = "CANCELADA"
    usuario.tipo_cuenta = "FREE"
    db.commit()
    db.refresh(suscripcion)
    return suscripcion
