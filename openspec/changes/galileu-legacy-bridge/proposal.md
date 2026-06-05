# Proposal: galileu-legacy-bridge

Adaptar importação Galileu para escrever no novo domínio (Pessoa + Matricula + Mensalidade) mantendo compatibilidade com tabela `alunos`.

## Entrega

- `services/galileu_import.py`
- `services/legacy_adapter.py` para rotas `/alunos/`
