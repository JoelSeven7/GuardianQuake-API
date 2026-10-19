from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.schemas import UsuarioRegistro, UsuarioOut, Token
from app.security import obtener_usuario_actual
from app.crud import usuarios as crud_usuarios

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])


@router.post("/registro", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def registro(datos: UsuarioRegistro, db: Session = Depends(get_db)):
    return crud_usuarios.registrar_usuario(db, datos)


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    token = crud_usuarios.autenticar_usuario(db, form_data.username, form_data.password)
    return Token(access_token=token)


@router.get("/me", response_model=UsuarioOut)
def perfil(usuario=Depends(obtener_usuario_actual)):
    return usuario
