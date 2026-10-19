from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, Enum, Text, SmallInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True)
    correo = Column(String(150), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    tipo_cuenta = Column(Enum("FREE", "PRO", name="tipo_cuenta"), nullable=False, default="FREE")
    fecha_registro = Column(DateTime, server_default=func.now())

    dispositivos = relationship("Dispositivo", back_populates="usuario")
    eventos = relationship("EventoSismico", back_populates="usuario")
    suscripciones = relationship("Suscripcion", back_populates="usuario")
    contactos = relationship("ContactoEmergencia", back_populates="usuario")


class Dispositivo(Base):
    __tablename__ = "dispositivos"

    id_dispositivo = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    modelo = Column(String(100), nullable=False)
    fabricante = Column(String(100), nullable=False)
    so_version = Column(String(50))
    sensibilidad_recomendada = Column(Numeric(4, 2), default=5.00)
    fecha_registro = Column(DateTime, server_default=func.now())

    usuario = relationship("Usuario", back_populates="dispositivos")


class EventoSismico(Base):
    __tablename__ = "eventos_sismicos"

    id_evento = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_dispositivo = Column(Integer, ForeignKey("dispositivos.id_dispositivo"), nullable=True)
    fecha_hora = Column(DateTime, nullable=False)
    intensidad_aproximada = Column(Numeric(5, 2), nullable=False)
    duracion_ms = Column(Integer, nullable=False)
    sensibilidad_usada = Column(SmallInteger, nullable=False)
    fecha_registro = Column(DateTime, server_default=func.now())

    usuario = relationship("Usuario", back_populates="eventos")
    dispositivo = relationship("Dispositivo")


class ContenidoEducativo(Base):
    __tablename__ = "contenido_educativo"

    id_contenido = Column(Integer, primary_key=True)
    titulo = Column(String(200), nullable=False)
    cuerpo = Column(Text, nullable=False)
    version = Column(String(20), nullable=False, default="1.0")
    fecha_publicacion = Column(DateTime, server_default=func.now())


class Suscripcion(Base):
    __tablename__ = "suscripciones"

    id_suscripcion = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    tipo = Column(Enum("PRO", name="tipo_suscripcion"), nullable=False, default="PRO")
    fecha_inicio = Column(DateTime, server_default=func.now())
    fecha_fin = Column(DateTime, nullable=True)
    estado = Column(Enum("ACTIVA", "CANCELADA", "EXPIRADA", name="estado_suscripcion"), nullable=False, default="ACTIVA")
    id_transaccion = Column(String(100), nullable=False)
    plataforma = Column(Enum("GOOGLE_PLAY", name="plataforma_pago"), nullable=False, default="GOOGLE_PLAY")

    usuario = relationship("Usuario", back_populates="suscripciones")


class ContactoEmergencia(Base):
    __tablename__ = "contactos_emergencia"

    id_contacto = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    nombre = Column(String(150), nullable=False)
    telefono = Column(String(20), nullable=False)

    usuario = relationship("Usuario", back_populates="contactos")
