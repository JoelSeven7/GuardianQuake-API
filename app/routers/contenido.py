from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.schemas import ContenidoEducativoOut
from app.crud import contenido as crud_contenido

router = APIRouter(prefix="/api/contenido-educativo", tags=["Contenido educativo"])


@router.get("", response_model=List[ContenidoEducativoOut])
def listar(db: Session = Depends(get_db)):
    return crud_contenido.listar_contenido(db)


@router.get("/{id_contenido}", response_model=ContenidoEducativoOut)
def detalle(id_contenido: int, db: Session = Depends(get_db)):
    return crud_contenido.obtener_contenido(db, id_contenido)
