from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


# ---------- Usuarios / Auth ----------
class UsuarioRegistro(BaseModel):
    correo: EmailStr
    password: str = Field(min_length=6)


class UsuarioLogin(BaseModel):
    correo: EmailStr
    password: str


class UsuarioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_usuario: int
    correo: EmailStr
    tipo_cuenta: str
    fecha_registro: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- Dispositivos ----------
class DispositivoCrear(BaseModel):
    modelo: str
    fabricante: str
    so_version: Optional[str] = None


class DispositivoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_dispositivo: int
    modelo: str
    fabricante: str
    so_version: Optional[str]
    sensibilidad_recomendada: float
    fecha_registro: datetime


class CalibracionOut(BaseModel):
    id_dispositivo: int
    modelo: str
    fabricante: str
    sensibilidad_recomendada: float


# ---------- Eventos sismicos ----------
class EventoSismicoCrear(BaseModel):
    id_dispositivo: Optional[int] = None
    fecha_hora: datetime
    intensidad_aproximada: float
    duracion_ms: int
    sensibilidad_usada: int = Field(ge=1, le=10)


class EventoSismicoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_evento: int
    id_dispositivo: Optional[int]
    fecha_hora: datetime
    intensidad_aproximada: float
    duracion_ms: int
    sensibilidad_usada: int
    fecha_registro: datetime


# ---------- Contenido educativo ----------
class ContenidoEducativoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_contenido: int
    titulo: str
    cuerpo: str
    version: str
    fecha_publicacion: datetime


# ---------- Suscripcion ----------
class VerificarCompraIn(BaseModel):
    id_transaccion: str
    plataforma: str = "GOOGLE_PLAY"


class SuscripcionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_suscripcion: int
    tipo: str
    fecha_inicio: datetime
    fecha_fin: Optional[datetime]
    estado: str
    plataforma: str


class EstadoSuscripcionOut(BaseModel):
    tipo_cuenta: str
    suscripcion: Optional[SuscripcionOut] = None


# ---------- Contactos de emergencia ----------
class ContactoEmergenciaIn(BaseModel):
    nombre: str
    telefono: str


class ContactoEmergenciaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_contacto: int
    nombre: str
    telefono: str
