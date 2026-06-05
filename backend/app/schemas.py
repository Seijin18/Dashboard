from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date


# --- Legado ---
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
    aluno_id: Optional[int] = None
    matricula_id: Optional[int] = None


class MensalidadeUpdate(BaseModel):
    contrato_num: Optional[str] = None
    mes_referencia: Optional[str] = None
    data_vencimento: Optional[date] = None
    data_pagamento: Optional[date] = None
    valor_previsto: Optional[float] = None
    valor_pago: Optional[float] = None
    taxa_bancaria: Optional[float] = None
    status: Optional[str] = None


class Mensalidade(MensalidadeBase):
    id: int
    aluno_id: Optional[int] = None
    matricula_id: Optional[int] = None

    class Config:
        from_attributes = True


class AlunoComHistorico(Aluno):
    mensalidades: List[Mensalidade]

    class Config:
        from_attributes = True


# --- Novo domínio ---
class AssociacaoBase(BaseModel):
    nome: str
    slug: str


class Associacao(AssociacaoBase):
    id: int

    class Config:
        from_attributes = True


class ModalidadeBase(BaseModel):
    nome: str
    slug: str
    ativa: bool = True


class ModalidadeCreate(ModalidadeBase):
    associacao_id: int = 1


class Modalidade(ModalidadeBase):
    id: int
    associacao_id: int

    class Config:
        from_attributes = True


class TurmaBase(BaseModel):
    nome: str
    horario: Optional[str] = None


class TurmaCreate(TurmaBase):
    modalidade_id: int


class Turma(TurmaBase):
    id: int
    modalidade_id: int

    class Config:
        from_attributes = True


class TurmaComModalidade(Turma):
    modalidade_nome: Optional[str] = None


class PessoaBase(BaseModel):
    nome: str
    email: Optional[str] = None
    telefone: Optional[str] = None
    titular_id: Optional[int] = None


class PessoaCreate(PessoaBase):
    pass


class PessoaUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    titular_id: Optional[int] = None


class Pessoa(PessoaBase):
    id: int

    class Config:
        from_attributes = True


class MatriculaBase(BaseModel):
    pessoa_id: int
    turma_id: int
    status: str = "Ativa"
    data_inicio: Optional[date] = None


class MatriculaCreate(MatriculaBase):
    pass


class MatriculaUpdate(BaseModel):
    status: Optional[str] = None
    turma_id: Optional[int] = None
    data_inicio: Optional[date] = None


class Matricula(MatriculaBase):
    id: int
    legacy_aluno_id: Optional[int] = None

    class Config:
        from_attributes = True


class MatriculaComDetalhes(Matricula):
    turma_nome: Optional[str] = None
    modalidade_nome: Optional[str] = None
    pessoa_nome: Optional[str] = None


class PessoaComMatriculas(Pessoa):
    matriculas: List[MatriculaComDetalhes] = []


class MensalidadeComDetalhes(Mensalidade):
    pessoa_nome: Optional[str] = None
    modalidade_nome: Optional[str] = None
    turma_nome: Optional[str] = None


# --- Auth ---
class UserCreate(BaseModel):
    email: str
    password: str
    role: str = "admin"


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    email: str
    role: str

    class Config:
        from_attributes = True


# --- Métricas ---
class MetricasGlobais(BaseModel):
    total_pessoas: int
    matriculas_ativas: int
    receita_prevista: float
    receita_recebida: float
    por_modalidade: List[dict] = Field(default_factory=list)
