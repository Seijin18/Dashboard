# Financial Ingestion (Galileu PDF)

## Overview

Ingestão de relatórios PDF do sistema Galileu com fluxo em duas etapas: preview (sem persistência) e confirmação (persistência).

## Requirements

### Requirement: PDF preview without side effects

O sistema DEVE analisar um PDF Galileu e classificar registros sem gravar no banco.

#### Scenario: Novo aluno no PDF

- **GIVEN** um PDF com aluno inexistente no banco
- **WHEN** o operador envia o ficheiro para `POST /upload-pdf-preview/`
- **THEN** o registro aparece em `novos`
- **AND** nenhum dado é persistido

#### Scenario: Mensalidade atualizada

- **GIVEN** um aluno existente com mensalidade na mesma data e contrato
- **WHEN** o status ou valor pago mudou no PDF
- **THEN** o registro aparece em `atualizados` com `_old_status` e `_old_valor_pago`

#### Scenario: Registro inalterado

- **GIVEN** dados idênticos no PDF e no banco
- **WHEN** o preview é executado
- **THEN** o registro aparece em `inalterados`

### Requirement: Confirmação de importação

O sistema DEVE persistir apenas os registros aprovados pelo operador.

#### Scenario: Confirmação de novos registros

- **GIVEN** uma lista de registros em `novos` do preview
- **WHEN** o operador envia `POST /upload-pdf-confirm/`
- **THEN** pessoas/matrículas e mensalidades são criadas ou atualizadas
- **AND** a resposta indica quantidade processada

### Requirement: Deduplicação de alunos

O sistema DEVE identificar alunos por `(nome_cliente, dependente)` para evitar duplicidade de matrículas de dependentes.

#### Scenario: Dois filhos do mesmo titular

- **GIVEN** dois registros com mesmo `nome_cliente` e `dependente` diferentes
- **WHEN** importados
- **THEN** são tratados como pessoas distintas

## API

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/upload-pdf-preview/` | Parse + diff |
| POST | `/upload-pdf-confirm/` | Persistência |

## Componentes

- `backend/app/pdf_parser.py` — extração regex/pdfplumber
- `backend/app/services/galileu_import.py` — bridge para domínio multi-modalidade
