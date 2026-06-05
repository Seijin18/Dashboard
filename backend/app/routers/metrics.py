from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/", response_model=schemas.MetricasGlobais)
def get_metrics(db: Session = Depends(get_db)):
    total_pessoas = db.query(models.Pessoa).count()
    matriculas_ativas = db.query(models.Matricula).filter(models.Matricula.status == "Ativa").count()

    receita_prevista = db.query(func.coalesce(func.sum(models.Mensalidade.valor_previsto), 0.0)).scalar() or 0.0
    receita_recebida = (
        db.query(func.coalesce(func.sum(models.Mensalidade.valor_pago), 0.0))
        .filter(models.Mensalidade.valor_pago.isnot(None))
        .scalar()
        or 0.0
    )

    por_modalidade = []
    modalidades = db.query(models.Modalidade).filter(models.Modalidade.ativa.is_(True)).all()
    for mod in modalidades:
        matriculas = (
            db.query(models.Matricula)
            .join(models.Turma)
            .filter(models.Turma.modalidade_id == mod.id, models.Matricula.status == "Ativa")
            .count()
        )
        receita_mod = (
            db.query(func.coalesce(func.sum(models.Mensalidade.valor_previsto), 0.0))
            .join(models.Matricula)
            .join(models.Turma)
            .filter(models.Turma.modalidade_id == mod.id)
            .scalar()
            or 0.0
        )
        por_modalidade.append({
            "modalidade_id": mod.id,
            "modalidade_nome": mod.nome,
            "matriculas_ativas": matriculas,
            "receita_prevista": receita_mod,
        })

    return schemas.MetricasGlobais(
        total_pessoas=total_pessoas,
        matriculas_ativas=matriculas_ativas,
        receita_prevista=receita_prevista,
        receita_recebida=receita_recebida,
        por_modalidade=por_modalidade,
    )
