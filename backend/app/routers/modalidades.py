from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import models, schemas
from ..auth_utils import require_admin

router = APIRouter(prefix="/modalidades", tags=["modalidades"])


@router.get("/", response_model=List[schemas.Modalidade])
def list_modalidades(db: Session = Depends(get_db)):
    return db.query(models.Modalidade).all()


@router.post("/", response_model=schemas.Modalidade)
def create_modalidade(
    payload: schemas.ModalidadeCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_admin),
):
    existing = db.query(models.Modalidade).filter(models.Modalidade.slug == payload.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Slug já existe")
    modalidade = models.Modalidade(**payload.model_dump())
    db.add(modalidade)
    db.commit()
    db.refresh(modalidade)
    return modalidade
