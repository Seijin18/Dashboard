from sqlalchemy.orm import Session
from .. import models


def list_alunos_legacy(db: Session, skip: int = 0, limit: int = 100) -> list:
    """Lista alunos no formato legado, priorizando dados do novo domínio quando disponível."""
    pessoas = db.query(models.Pessoa).offset(skip).limit(limit).all()
    if pessoas:
        return [_pessoa_to_legacy_item(db, p) for p in pessoas]

    alunos_db = db.query(models.Aluno).offset(skip).limit(limit).all()
    resultado = []
    for a in alunos_db:
        resultado.append(_aluno_to_legacy_item(db, a))
    return resultado


def get_aluno_legacy(db: Session, aluno_id: int):
    matricula = db.query(models.Matricula).filter(
        models.Matricula.legacy_aluno_id == aluno_id
    ).first()
    if matricula:
        return _pessoa_to_aluno_com_historico(db, matricula.pessoa, aluno_id)

    aluno = db.query(models.Aluno).filter(models.Aluno.id == aluno_id).first()
    return aluno


def _pessoa_to_legacy_item(db: Session, pessoa: models.Pessoa) -> dict:
    matriculas = db.query(models.Matricula).filter(models.Matricula.pessoa_id == pessoa.id).all()
    mensalidades = []
    for m in matriculas:
        mensalidades.extend(
            db.query(models.Mensalidade)
            .filter(models.Mensalidade.matricula_id == m.id)
            .order_by(models.Mensalidade.data_vencimento.desc())
            .all()
        )

    if not mensalidades:
        legacy_id = matriculas[0].legacy_aluno_id if matriculas else pessoa.id
        return {
            "id": legacy_id or pessoa.id,
            "nome": pessoa.nome,
            "contrato": "S/N",
            "modalidade": matriculas[0].turma.nome if matriculas else "—",
            "plano": "Mensal",
            "status": matriculas[0].status if matriculas else "Ativa",
            "valor": 0.0,
            "pre_inscricao": False,
        }

    mensalidade_efetiva = next(
        (m for m in mensalidades if m.contrato_num or m.valor_previsto > 0), None
    )
    ultima = mensalidade_efetiva or mensalidades[0]
    teve_pre = any(not m.contrato_num and m.valor_previsto == 0 for m in mensalidades) and len(mensalidades) > 1

    turma_nome = "—"
    if matriculas:
        turma = db.query(models.Turma).filter(models.Turma.id == matriculas[0].turma_id).first()
        if turma:
            turma_nome = turma.nome

    legacy_id = matriculas[0].legacy_aluno_id if matriculas else pessoa.id

    return {
        "id": legacy_id or pessoa.id,
        "nome": pessoa.nome,
        "contrato": ultima.contrato_num if ultima and ultima.contrato_num else "S/N",
        "modalidade": ultima.mes_referencia if ultima and not ultima.contrato_num and ultima.valor_previsto > 0 else turma_nome,
        "plano": "Mensal",
        "status": ultima.status if ultima else "Ativa",
        "valor": ultima.valor_previsto if ultima else 0.0,
        "pre_inscricao": teve_pre,
    }


def _aluno_to_legacy_item(db: Session, a: models.Aluno) -> dict:
    mensalidades = (
        db.query(models.Mensalidade)
        .filter(models.Mensalidade.aluno_id == a.id)
        .order_by(models.Mensalidade.data_vencimento.desc())
        .all()
    )
    mensalidade_efetiva = next(
        (m for m in mensalidades if m.contrato_num or m.valor_previsto > 0), None
    )
    ultima = mensalidade_efetiva or (mensalidades[0] if mensalidades else None)
    teve_pre = any(not m.contrato_num and m.valor_previsto == 0 for m in mensalidades) and len(mensalidades) > 1
    nome_exibicao = a.dependente if a.dependente else a.nome_cliente

    return {
        "id": a.id,
        "nome": nome_exibicao,
        "contrato": ultima.contrato_num if ultima and ultima.contrato_num else "S/N",
        "modalidade": ultima.mes_referencia if ultima and not ultima.contrato_num and ultima.valor_previsto > 0 else a.grupo_inscricao,
        "plano": "Mensal",
        "status": ultima.status if ultima else a.status_matricula,
        "valor": ultima.valor_previsto if ultima else 0.0,
        "pre_inscricao": teve_pre,
    }


def _pessoa_to_aluno_com_historico(db: Session, pessoa: models.Pessoa, legacy_id: int):
    matricula = db.query(models.Matricula).filter(models.Matricula.pessoa_id == pessoa.id).first()
    turma_nome = matricula.turma.nome if matricula and matricula.turma else "Geral"

    mensalidades = []
    for m in db.query(models.Matricula).filter(models.Matricula.pessoa_id == pessoa.id).all():
        mensalidades.extend(
            db.query(models.Mensalidade).filter(models.Mensalidade.matricula_id == m.id).all()
        )

    titular_nome = pessoa.titular.nome if pessoa.titular_id and pessoa.titular else pessoa.nome

    class AlunoCompat:
        def __init__(self):
            self.id = legacy_id
            self.nome_cliente = titular_nome
            self.dependente = pessoa.nome if pessoa.titular_id else None
            self.grupo_inscricao = turma_nome
            self.status_matricula = matricula.status if matricula else "Ativa"
            self.mensalidades = sorted(mensalidades, key=lambda x: x.data_vencimento, reverse=True)

    return AlunoCompat()
