from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from .. import models, schemas
from ..auth_utils import require_admin

router = APIRouter(prefix="/pessoas", tags=["pessoas"])


def _matricula_detalhes(db: Session, matricula: models.Matricula) -> schemas.MatriculaComDetalhes:
    item = schemas.MatriculaComDetalhes.model_validate(matricula)
    if matricula.turma:
        item.turma_nome = matricula.turma.nome
        if matricula.turma.modalidade:
            item.modalidade_nome = matricula.turma.modalidade.nome
    if matricula.pessoa:
        item.pessoa_nome = matricula.pessoa.nome
    return item


@router.get("/", response_model=List[schemas.Pessoa])
def list_pessoas(
    skip: int = 0,
    limit: int = 100,
    q: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Pessoa)
    if q:
        query = query.filter(models.Pessoa.nome.ilike(f"%{q}%"))
    return query.offset(skip).limit(limit).all()


@router.post("/", response_model=schemas.Pessoa)
def create_pessoa(
    payload: schemas.PessoaCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_admin),
):
    if payload.titular_id:
        titular = db.query(models.Pessoa).filter(models.Pessoa.id == payload.titular_id).first()
        if not titular:
            raise HTTPException(status_code=404, detail="Titular não encontrado")
    pessoa = models.Pessoa(**payload.model_dump())
    db.add(pessoa)
    db.commit()
    db.refresh(pessoa)
    return pessoa


@router.get("/{pessoa_id}", response_model=schemas.PessoaComMatriculas)
def get_pessoa(pessoa_id: int, db: Session = Depends(get_db)):
    pessoa = db.query(models.Pessoa).filter(models.Pessoa.id == pessoa_id).first()
    if not pessoa:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    matriculas = db.query(models.Matricula).filter(models.Matricula.pessoa_id == pessoa_id).all()
    result = schemas.PessoaComMatriculas.model_validate(pessoa)
    result.matriculas = [_matricula_detalhes(db, m) for m in matriculas]
    return result


@router.patch("/{pessoa_id}", response_model=schemas.Pessoa)
def update_pessoa(
    pessoa_id: int,
    payload: schemas.PessoaUpdate,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_admin),
):
    pessoa = db.query(models.Pessoa).filter(models.Pessoa.id == pessoa_id).first()
    if not pessoa:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(pessoa, key, value)
    db.commit()
    db.refresh(pessoa)
    return pessoa


@router.get("/{pessoa_id}/matriculas", response_model=List[schemas.MatriculaComDetalhes])
def list_matriculas_pessoa(pessoa_id: int, db: Session = Depends(get_db)):
    pessoa = db.query(models.Pessoa).filter(models.Pessoa.id == pessoa_id).first()
    if not pessoa:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    matriculas = db.query(models.Matricula).filter(models.Matricula.pessoa_id == pessoa_id).all()
    return [_matricula_detalhes(db, m) for m in matriculas]
