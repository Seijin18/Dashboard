from datetime import date
from sqlalchemy.orm import Session
from .. import models


def _get_or_create_titular(db: Session, nome_cliente: str) -> models.Pessoa:
    titular = db.query(models.Pessoa).filter(
        models.Pessoa.nome == nome_cliente,
        models.Pessoa.titular_id.is_(None),
    ).first()
    if not titular:
        titular = models.Pessoa(nome=nome_cliente)
        db.add(titular)
        db.flush()
    return titular


def _get_or_create_pessoa_from_aluno(db: Session, aluno: models.Aluno) -> models.Pessoa:
    if aluno.dependente:
        titular = _get_or_create_titular(db, aluno.nome_cliente)
        pessoa = db.query(models.Pessoa).filter(
            models.Pessoa.nome == aluno.dependente,
            models.Pessoa.titular_id == titular.id,
        ).first()
        if not pessoa:
            pessoa = models.Pessoa(nome=aluno.dependente, titular_id=titular.id)
            db.add(pessoa)
            db.flush()
        return pessoa

    return _get_or_create_titular(db, aluno.nome_cliente)


def _get_or_create_turma_judo(db: Session, grupo_inscricao: str) -> models.Turma:
    modalidade = db.query(models.Modalidade).filter(models.Modalidade.slug == "judo").first()
    if not modalidade:
        raise ValueError("Modalidade Judô não encontrada. Execute seed_defaults primeiro.")

    turma = db.query(models.Turma).filter(
        models.Turma.modalidade_id == modalidade.id,
        models.Turma.nome == grupo_inscricao,
    ).first()
    if not turma:
        turma = models.Turma(modalidade_id=modalidade.id, nome=grupo_inscricao)
        db.add(turma)
        db.flush()
    return turma


def migrate_alunos_to_domain(db: Session) -> dict:
    """Migra registros legados Aluno/Mensalidade para Pessoa/Matricula/Mensalidade."""
    migrated_pessoas = 0
    migrated_matriculas = 0
    migrated_mensalidades = 0

    alunos = db.query(models.Aluno).all()
    for aluno in alunos:
        pessoa = _get_or_create_pessoa_from_aluno(db, aluno)
        migrated_pessoas += 1

        turma = _get_or_create_turma_judo(db, aluno.grupo_inscricao or "Geral")

        matricula = db.query(models.Matricula).filter(
            models.Matricula.legacy_aluno_id == aluno.id,
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
                status=aluno.status_matricula,
                data_inicio=date.today(),
                legacy_aluno_id=aluno.id,
            )
            db.add(matricula)
            db.flush()
            migrated_matriculas += 1

        for mens in db.query(models.Mensalidade).filter(models.Mensalidade.aluno_id == aluno.id).all():
            if not mens.matricula_id:
                mens.matricula_id = matricula.id
                migrated_mensalidades += 1

    db.commit()
    return {
        "pessoas": migrated_pessoas,
        "matriculas": migrated_matriculas,
        "mensalidades": migrated_mensalidades,
        "alunos_processados": len(alunos),
    }
