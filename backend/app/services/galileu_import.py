from datetime import datetime
from typing import Any, Dict, List
from sqlalchemy.orm import Session
from .. import models
from .migration import _get_or_create_pessoa_from_aluno, _get_or_create_turma_judo


def _parse_date(value):
    if isinstance(value, str):
        return datetime.fromisoformat(value).date()
    return value


def _find_or_create_aluno_legacy(db: Session, aluno_info: dict) -> models.Aluno:
    aluno_db = db.query(models.Aluno).filter(
        models.Aluno.nome_cliente == aluno_info["nome_cliente"],
        models.Aluno.dependente == aluno_info.get("dependente"),
    ).first()
    if not aluno_db:
        aluno_db = models.Aluno(**aluno_info)
        db.add(aluno_db)
        db.flush()
    else:
        aluno_db.grupo_inscricao = aluno_info.get("grupo_inscricao", aluno_db.grupo_inscricao)
        aluno_db.status_matricula = aluno_info.get("status_matricula", aluno_db.status_matricula)
    return aluno_db


def _find_or_create_matricula(db: Session, aluno_info: dict, aluno_db: models.Aluno) -> models.Matricula:
    pessoa = _get_or_create_pessoa_from_aluno(db, aluno_db)
    turma = _get_or_create_turma_judo(db, aluno_info.get("grupo_inscricao", "Geral"))

    matricula = db.query(models.Matricula).filter(
        models.Matricula.legacy_aluno_id == aluno_db.id,
    ).first()
    if not matricula:
        matricula = db.query(models.Matricula).filter(
            models.Matricula.pessoa_id == pessoa.id,
            models.Matricula.turma_id == turma.id,
        ).first()
    if not matricula:
        matricula = models.Matricula(
            pessoa_id=pessoa.id,
            turma_id=turma.id,
            status=aluno_info.get("status_matricula", "Ativa"),
            legacy_aluno_id=aluno_db.id,
        )
        db.add(matricula)
        db.flush()
    return matricula


def preview_registros(db: Session, registros: List[Dict[str, Any]]) -> dict:
    novos, atualizados, inalterados = [], [], []

    for rw in registros:
        aluno_info = rw["aluno"]
        mens_info = rw["mensalidade"]

        aluno_db = db.query(models.Aluno).filter(
            models.Aluno.nome_cliente == aluno_info["nome_cliente"],
            models.Aluno.dependente == aluno_info.get("dependente"),
        ).first()

        if not aluno_db:
            novos.append(rw)
            continue

        mensalidade_db = db.query(models.Mensalidade).filter(
            models.Mensalidade.aluno_id == aluno_db.id,
            models.Mensalidade.data_vencimento == mens_info["data_vencimento"],
            models.Mensalidade.contrato_num == mens_info["contrato_num"],
        ).first()

        if not mensalidade_db:
            novos.append(rw)
        elif (
            mensalidade_db.status != mens_info["status"]
            or mensalidade_db.valor_pago != mens_info.get("valor_pago")
            or mensalidade_db.data_pagamento != mens_info.get("data_pagamento")
        ):
            rw["_old_status"] = mensalidade_db.status
            rw["_old_valor_pago"] = mensalidade_db.valor_pago
            atualizados.append(rw)
        else:
            inalterados.append(rw)

    return {
        "novos": novos,
        "atualizados": atualizados,
        "inalterados": inalterados,
        "total_encontrados": len(registros),
    }


def confirm_registros(db: Session, registros: List[Dict[str, Any]]) -> int:
    processados = 0
    for rw in registros:
        aluno_info = rw["aluno"]
        mens_info = dict(rw["mensalidade"])

        mens_info["data_vencimento"] = _parse_date(mens_info["data_vencimento"])
        if mens_info.get("data_pagamento"):
            mens_info["data_pagamento"] = _parse_date(mens_info["data_pagamento"])

        aluno_db = _find_or_create_aluno_legacy(db, aluno_info)
        matricula = _find_or_create_matricula(db, aluno_info, aluno_db)

        mensalidade_db = db.query(models.Mensalidade).filter(
            models.Mensalidade.aluno_id == aluno_db.id,
            models.Mensalidade.data_vencimento == mens_info["data_vencimento"],
            models.Mensalidade.contrato_num == mens_info["contrato_num"],
        ).first()

        if not mensalidade_db:
            nova = models.Mensalidade(**mens_info, aluno_id=aluno_db.id, matricula_id=matricula.id)
            db.add(nova)
        else:
            mensalidade_db.status = mens_info["status"]
            mensalidade_db.valor_pago = mens_info.get("valor_pago")
            mensalidade_db.data_pagamento = mens_info.get("data_pagamento")
            mensalidade_db.matricula_id = matricula.id

        processados += 1

    db.commit()
    return processados
