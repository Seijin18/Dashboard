from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from .database import Base


class Associacao(Base):
    __tablename__ = "associacoes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True)

    modalidades = relationship("Modalidade", back_populates="associacao")


class Modalidade(Base):
    __tablename__ = "modalidades"

    id = Column(Integer, primary_key=True, index=True)
    associacao_id = Column(Integer, ForeignKey("associacoes.id"), nullable=False)
    nome = Column(String, nullable=False)
    slug = Column(String, index=True)
    ativa = Column(Boolean, default=True)

    associacao = relationship("Associacao", back_populates="modalidades")
    turmas = relationship("Turma", back_populates="modalidade")


class Turma(Base):
    __tablename__ = "turmas"

    id = Column(Integer, primary_key=True, index=True)
    modalidade_id = Column(Integer, ForeignKey("modalidades.id"), nullable=False)
    nome = Column(String, nullable=False)
    horario = Column(String, nullable=True)

    modalidade = relationship("Modalidade", back_populates="turmas")
    matriculas = relationship("Matricula", back_populates="turma")


class Pessoa(Base):
    __tablename__ = "pessoas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    email = Column(String, nullable=True)
    telefone = Column(String, nullable=True)
    titular_id = Column(Integer, ForeignKey("pessoas.id"), nullable=True)

    titular = relationship("Pessoa", remote_side="Pessoa.id", backref="dependentes")
    matriculas = relationship("Matricula", back_populates="pessoa")


class Matricula(Base):
    __tablename__ = "matriculas"

    id = Column(Integer, primary_key=True, index=True)
    pessoa_id = Column(Integer, ForeignKey("pessoas.id"), nullable=False)
    turma_id = Column(Integer, ForeignKey("turmas.id"), nullable=False)
    status = Column(String, default="Ativa")
    data_inicio = Column(Date, nullable=True)
    legacy_aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=True)

    pessoa = relationship("Pessoa", back_populates="matriculas")
    turma = relationship("Turma", back_populates="matriculas")
    mensalidades = relationship("Mensalidade", back_populates="matricula")


class Aluno(Base):
    """Legado — mantido para compatibilidade durante transição."""

    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    nome_cliente = Column(String, index=True)
    dependente = Column(String, nullable=True)
    grupo_inscricao = Column(String)
    status_matricula = Column(String, default="Ativa")

    mensalidades = relationship("Mensalidade", back_populates="aluno", foreign_keys="Mensalidade.aluno_id")


class Mensalidade(Base):
    __tablename__ = "mensalidades"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=True)
    matricula_id = Column(Integer, ForeignKey("matriculas.id"), nullable=True)
    contrato_num = Column(String, nullable=True)
    mes_referencia = Column(String)
    data_vencimento = Column(Date)
    data_pagamento = Column(Date, nullable=True)
    valor_previsto = Column(Float)
    valor_pago = Column(Float, nullable=True)
    taxa_bancaria = Column(Float, default=1.99)
    status = Column(String, default="Pendente")

    aluno = relationship("Aluno", back_populates="mensalidades", foreign_keys=[aluno_id])
    matricula = relationship("Matricula", back_populates="mensalidades")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="admin")
