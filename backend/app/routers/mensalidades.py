from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from .. import models, schemas
from ..auth_utils import require_admin

router = APIRouter(prefix="/mensalidades", tags=["mensalidades"])


def _mensalidade_detalhes(db: Session, mens: models.Mensalidade) -> schemas.MensalidadeComDetalhes:
    item = schemas.MensalidadeComDetalhes.model_validate(mens)
    if mens.matricula:
        if mens.matricula.pessoa:
            item.pessoa_nome = mens.matricula.pessoa.nome
        if mens.matricula.turma:
            item.turma_nome = mens.matricula.turma.nome
            if mens.matricula.turma.modalidade:
                item.modalidade_nome = mens.matricula.turma.modalidade.nome
    return item


@router.get("/", response_model=List[schemas.MensalidadeComDetalhes])
def list_mensalidades(
    matricula_id: Optional[int] = None,
    modalidade_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    q = db.query(models.Mensalidade)
    if matricula_id:
        q = q.filter(models.Mensalidade.matricula_id == matricula_id)
    if modalidade_id:
        q = q.join(models.Matricula).join(models.Turma).filter(
            models.Turma.modalidade_id == modalidade_id
        )
    return [_mensalidade_detalhes(db, m) for m in q.all()]


@router.post("/", response_model=schemas.Mensalidade)
def create_mensalidade(
    payload: schemas.MensalidadeCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_admin),
):
    if not payload.matricula_id:
        raise HTTPException(status_code=400, detail="matricula_id é obrigatório")
    matricula = db.query(models.Matricula).filter(models.Matricula.id == payload.matricula_id).first()
    if not matricula:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")

    data = payload.model_dump()
    data["aluno_id"] = matricula.legacy_aluno_id
    mensalidade = models.Mensalidade(**data)
    db.add(mensalidade)
    db.commit()
    db.refresh(mensalidade)
    return mensalidade


@router.patch("/{mensalidade_id}", response_model=schemas.Mensalidade)
def update_mensalidade(
    mensalidade_id: int,
    payload: schemas.MensalidadeUpdate,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_admin),
):
    mensalidade = db.query(models.Mensalidade).filter(models.Mensalidade.id == mensalidade_id).first()
    if not mensalidade:
        raise HTTPException(status_code=404, detail="Mensalidade não encontrada")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(mensalidade, key, value)
    db.commit()
    db.refresh(mensalidade)
    return mensalidade


@router.delete("/{mensalidade_id}")
def delete_mensalidade(
    mensalidade_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_admin),
):
    mensalidade = db.query(models.Mensalidade).filter(models.Mensalidade.id == mensalidade_id).first()
    if not mensalidade:
        raise HTTPException(status_code=404, detail="Mensalidade não encontrada")
    db.delete(mensalidade)
    db.commit()
    return {"status": "Mensalidade removida"}
