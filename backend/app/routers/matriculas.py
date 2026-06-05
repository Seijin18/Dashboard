from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from .. import models, schemas
from ..auth_utils import require_admin

router = APIRouter(prefix="/matriculas", tags=["matriculas"])


@router.get("/", response_model=List[schemas.MatriculaComDetalhes])
def list_matriculas(
    pessoa_id: Optional[int] = None,
    turma_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    q = db.query(models.Matricula)
    if pessoa_id:
        q = q.filter(models.Matricula.pessoa_id == pessoa_id)
    if turma_id:
        q = q.filter(models.Matricula.turma_id == turma_id)
    result = []
    for m in q.all():
        item = schemas.MatriculaComDetalhes.model_validate(m)
        if m.turma:
            item.turma_nome = m.turma.nome
            if m.turma.modalidade:
                item.modalidade_nome = m.turma.modalidade.nome
        if m.pessoa:
            item.pessoa_nome = m.pessoa.nome
        result.append(item)
    return result


@router.post("/", response_model=schemas.Matricula)
def create_matricula(
    payload: schemas.MatriculaCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_admin),
):
    pessoa = db.query(models.Pessoa).filter(models.Pessoa.id == payload.pessoa_id).first()
    if not pessoa:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    turma = db.query(models.Turma).filter(models.Turma.id == payload.turma_id).first()
    if not turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")

    existing = db.query(models.Matricula).filter(
        models.Matricula.pessoa_id == payload.pessoa_id,
        models.Matricula.turma_id == payload.turma_id,
        models.Matricula.status == "Ativa",
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Matrícula ativa já existe para esta turma")

    matricula = models.Matricula(**payload.model_dump())
    db.add(matricula)
    db.commit()
    db.refresh(matricula)
    return matricula


@router.patch("/{matricula_id}", response_model=schemas.Matricula)
def update_matricula(
    matricula_id: int,
    payload: schemas.MatriculaUpdate,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_admin),
):
    matricula = db.query(models.Matricula).filter(models.Matricula.id == matricula_id).first()
    if not matricula:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(matricula, key, value)
    db.commit()
    db.refresh(matricula)
    return matricula


@router.delete("/{matricula_id}")
def cancel_matricula(
    matricula_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_admin),
):
    matricula = db.query(models.Matricula).filter(models.Matricula.id == matricula_id).first()
    if not matricula:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")
    matricula.status = "Cancelada"
    db.commit()
    return {"status": "Matrícula cancelada"}
