from fastapi import FastAPI

from app.routers import usuarios, dispositivos, eventos, contenido, suscripcion, contactos

app = FastAPI(
    title="GuardianQuake API",
    description="Backend de respaldo, contenido y suscripcion para la app GuardianQuake "
                "(la deteccion sismica en si ocurre 100% offline en el dispositivo).",
    version="1.0.0",
)

app.include_router(usuarios.router)
app.include_router(dispositivos.router)
app.include_router(eventos.router)
app.include_router(contenido.router)
app.include_router(suscripcion.router)
app.include_router(contactos.router)


@app.get("/")
def index():
    return {
        "servicio": "GuardianQuake API",
        "estado": "activo",
        "docs": "/docs",
    }
