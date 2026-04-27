from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from .database import Base

class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    nome_cliente = Column(String, index=True)
    dependente = Column(String, nullable=True)
    grupo_inscricao = Column(String)
    status_matricula = Column(String, default="Ativa")

    mensalidades = relationship("Mensalidade", back_populates="aluno")

class Mensalidade(Base):
    __tablename__ = "mensalidades"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"))
    contrato_num = Column(String, nullable=True)
    mes_referencia = Column(String)
    data_vencimento = Column(Date)
    data_pagamento = Column(Date, nullable=True)
    valor_previsto = Column(Float)
    valor_pago = Column(Float, nullable=True)
    taxa_bancaria = Column(Float, default=1.99)
    status = Column(String, default="Pendente")

    aluno = relationship("Aluno", back_populates="mensalidades")