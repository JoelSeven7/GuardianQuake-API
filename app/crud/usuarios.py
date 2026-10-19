from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.models import Usuario
from app.schemas.schemas import UsuarioRegistro
from app.security import hash_password, verificar_password, crear_token


def registrar_usuario(db: Session, datos: UsuarioRegistro) -> Usuario:
    existente = db.query(Usuario).filter(Usuario.correo == datos.correo).first()
    if existente:
        raise HTTPException(status.HTTP_409_CONFLICT, "Ya existe una cuenta con ese correo")

    usuario = Usuario(correo=datos.correo, password_hash=hash_password(datos.password))
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def autenticar_usuario(db: Session, correo: str, password: str) -> str:
    usuario = db.query(Usuario).filter(Usuario.correo == correo).first()
    if not usuario or not verificar_password(password, usuario.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Correo o contraseña incorrectos")
    return crear_token(usuario.id_usuario)
