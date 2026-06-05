# Multi-Modality Domain

## Requirements

### Requirement: Modalidades configuráveis

O sistema DEVE permitir criar e listar modalidades (ex.: Judô, Yoga).

#### Scenario: Criar modalidade Yoga

- **GIVEN** associação Kannon Do existente
- **WHEN** admin cria modalidade "Yoga" via `POST /modalidades/`
- **THEN** modalidade fica disponível para turmas e matrículas

### Requirement: Matrícula cruzada

Uma pessoa DEVE poder ter múltiplas matrículas em turmas de modalidades diferentes.

#### Scenario: Aluno de judô matricula em yoga

- **GIVEN** pessoa com matrícula ativa em turma de Judô
- **WHEN** operador cria matrícula em turma de Yoga via `POST /matriculas/`
- **THEN** nova matrícula é criada sem duplicar a pessoa
- **AND** `GET /pessoas/{id}/matriculas` retorna ambas

### Requirement: Mensalidade por matrícula

Cada mensalidade DEVE ligar-se a uma matrícula específica.

#### Scenario: Cobrança independente por modalidade

- **GIVEN** pessoa com matrículas em Judô e Yoga
- **WHEN** mensalidades são criadas para cada matrícula
- **THEN** valores e status são independentes
