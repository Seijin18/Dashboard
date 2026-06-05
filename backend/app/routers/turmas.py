from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from .. import models, schemas
from ..auth_utils import require_admin

router = APIRouter(prefix="/turmas", tags=["turmas"])


@router.get("/", response_model=List[schemas.TurmaComModalidade])
def list_turmas(modalidade_id: Optional[int] = None, db: Session = Depends(get_db)):
    q = db.query(models.Turma)
    if modalidade_id:
        q = q.filter(models.Turma.modalidade_id == modalidade_id)
    turmas = q.all()
    result = []
    for t in turmas:
        item = schemas.TurmaComModalidade.model_validate(t)
        item.modalidade_nome = t.modalidade.nome if t.modalidade else None
        result.append(item)
    return result


@router.post("/", response_model=schemas.Turma)
def create_turma(
    payload: schemas.TurmaCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_admin),
):
    modalidade = db.query(models.Modalidade).filter(models.Modalidade.id == payload.modalidade_id).first()
    if not modalidade:
        raise HTTPException(status_code=404, detail="Modalidade não encontrada")
    turma = models.Turma(**payload.model_dump())
    db.add(turma)
    db.commit()
    db.refresh(turma)
    return turma
