# Proposal: data-migration-judo

Migração de dados legados `Aluno`/`Mensalidade` para `Pessoa`/`Matricula`/`Mensalidade.matricula_id`.

## Entrega

- `backend/app/services/migration.py`
- `POST /admin/migrate-legacy`
- Alembic revision `001_multi_modality_domain.py`
