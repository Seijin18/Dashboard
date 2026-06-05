"""multi_modality_domain

Revision ID: 001
Revises:
Create Date: 2026-06-05

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "associacoes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nome", sa.String(), nullable=False),
        sa.Column("slug", sa.String(), unique=True),
    )
    op.create_table(
        "modalidades",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("associacao_id", sa.Integer(), sa.ForeignKey("associacoes.id"), nullable=False),
        sa.Column("nome", sa.String(), nullable=False),
        sa.Column("slug", sa.String()),
        sa.Column("ativa", sa.Boolean(), default=True),
    )
    op.create_table(
        "turmas",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("modalidade_id", sa.Integer(), sa.ForeignKey("modalidades.id"), nullable=False),
        sa.Column("nome", sa.String(), nullable=False),
        sa.Column("horario", sa.String(), nullable=True),
    )
    op.create_table(
        "pessoas",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nome", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("telefone", sa.String(), nullable=True),
        sa.Column("titular_id", sa.Integer(), sa.ForeignKey("pessoas.id"), nullable=True),
    )
    op.create_table(
        "matriculas",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("pessoa_id", sa.Integer(), sa.ForeignKey("pessoas.id"), nullable=False),
        sa.Column("turma_id", sa.Integer(), sa.ForeignKey("turmas.id"), nullable=False),
        sa.Column("status", sa.String(), default="Ativa"),
        sa.Column("data_inicio", sa.Date(), nullable=True),
        sa.Column("legacy_aluno_id", sa.Integer(), sa.ForeignKey("alunos.id"), nullable=True),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(), unique=True, nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("role", sa.String(), default="admin"),
    )
    with op.batch_alter_table("mensalidades") as batch_op:
        batch_op.add_column(sa.Column("matricula_id", sa.Integer(), sa.ForeignKey("matriculas.id"), nullable=True))
        batch_op.alter_column("aluno_id", existing_type=sa.Integer(), nullable=True)


def downgrade() -> None:
    with op.batch_alter_table("mensalidades") as batch_op:
        batch_op.drop_column("matricula_id")
    op.drop_table("users")
    op.drop_table("matriculas")
    op.drop_table("pessoas")
    op.drop_table("turmas")
    op.drop_table("modalidades")
    op.drop_table("associacoes")
