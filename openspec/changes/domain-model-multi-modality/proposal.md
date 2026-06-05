# Proposal: domain-model-multi-modality

## What

Introduzir modelo de domínio multi-modalidade: Associacao, Modalidade, Turma, Pessoa, Matricula e Mensalidade ligada a matrícula.

## Why

O modelo atual (`Aluno` + `Mensalidade`) mistura pessoa com matrícula/turma e impede matrículas cruzadas (ex.: judô + yoga).

## Scope

- Novos modelos SQLAlchemy e schemas Pydantic
- Alembic para migrações
- Seed: Kannon Do + modalidade Judô
- Compat layer para rotas legadas `/alunos/`

## Decisões

- Uma associação (Kannon Do), sem multi-tenant
- Gestão manual unificada; Galileo como ponte legada
