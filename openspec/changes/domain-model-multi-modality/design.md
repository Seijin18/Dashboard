# Design: domain-model-multi-modality

## Modelo de dados

```
Associacao 1──* Modalidade 1──* Turma 1──* Matricula *──1 Pessoa
Matricula 1──* Mensalidade
Pessoa *──1 Pessoa (titular_id, self-ref para dependentes)
```

## Mapeamento legado

| Legado | Novo |
|--------|------|
| `Aluno.nome_cliente` (sem dependente) | `Pessoa` titular |
| `Aluno.dependente` | `Pessoa` dependente com `titular_id` |
| `Aluno.grupo_inscricao` | `Turma.nome` em `Modalidade` Judô |
| `Mensalidade.aluno_id` | `Mensalidade.matricula_id` |

## Compatibilidade

- Tabela `alunos` mantida; campo `legacy_aluno_id` em `Matricula` para rastreio
- `GET /alunos/` adaptado via `legacy_adapter.py`
- Import Galileu via `galileu_import.py` escreve no novo domínio

## Migrações

Alembic revision inicial cria todas as tabelas. Script `services/migration.py` converte dados existentes.
