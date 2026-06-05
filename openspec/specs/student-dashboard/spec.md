# Student Dashboard

## Overview

Dashboard financeiro com listagem de alunos, métricas, filtros e página de detalhes com histórico de mensalidades.

## Requirements

### Requirement: Listagem de alunos

O sistema DEVE exibir alunos com nome, contrato, modalidade/turma, plano, status e valor.

#### Scenario: Lista vazia

- **GIVEN** banco sem alunos
- **WHEN** o frontend chama `GET /alunos/`
- **THEN** retorna lista vazia

#### Scenario: Aluno com pré-inscrição e matrícula

- **GIVEN** aluno com mensalidade de pré-inscrição (valor 0) e contrato efetivo
- **WHEN** listado no dashboard
- **THEN** exibe dados da matrícula efetiva
- **AND** badge `pre_inscricao` quando aplicável

### Requirement: Detalhes do aluno

O sistema DEVE exibir perfil e histórico completo de mensalidades.

#### Scenario: Histórico de pagamentos

- **GIVEN** aluno com múltiplas mensalidades
- **WHEN** o operador abre `/alunos/{id}` ou `/pessoas/{id}`
- **THEN** vê todas as mensalidades ordenadas por vencimento

### Requirement: Filtros e busca

O dashboard DEVE permitir busca por nome/contrato e filtro por status.

#### Scenario: Busca por nome

- **GIVEN** lista de alunos carregada
- **WHEN** o operador digita no campo de busca
- **THEN** a tabela filtra em tempo real

## Frontend

| Rota | Componente | Função |
|------|------------|--------|
| `/` | `page.tsx` | Dashboard principal |
| `/alunos/[id]` | `alunos/[id]/page.tsx` | Detalhe legado |
| `/pessoas` | `pessoas/page.tsx` | Lista unificada |
| `/pessoas/[id]` | `pessoas/[id]/page.tsx` | Perfil multi-modalidade |
