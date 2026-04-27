from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class AlunoBase(BaseModel):
    nome_cliente: str
    dependente: Optional[str] = None
    grupo_inscricao: str
    status_matricula: str = "Ativa"

class AlunoCreate(AlunoBase):
    pass

class Aluno(AlunoBase):
    id: int

    class Config:
        from_attributes = True

class MensalidadeBase(BaseModel):
    contrato_num: Optional[str] = None
    mes_referencia: str
    data_vencimento: date
    data_pagamento: Optional[date] = None
    valor_previsto: float
    valor_pago: Optional[float] = None
    taxa_bancaria: float = 1.99
    status: str = "Pendente"

class MensalidadeCreate(MensalidadeBase):
    aluno_id: int

class Mensalidade(MensalidadeBase):
    id: int
    aluno_id: int

    class Config:
        from_attributes = True