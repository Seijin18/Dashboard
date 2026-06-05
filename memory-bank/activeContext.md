# Active Context

## Foco atual

SaaS multi-modalidade implementado: domínio Pessoa/Matricula/Modalidade/Turma, CRUD API, dashboard UI, billing manual, bridge Galileu e auth JWT.

## Estado

- OpenSpec: specs em `openspec/specs/`, changes em `openspec/changes/`
- Backend: routers em `backend/app/routers/`, serviços em `backend/app/services/`
- Frontend: `/pessoas`, `/modalidades`, `/turmas`, `/login`
- Testes: 8 passed (`make test` / pytest)

## Credenciais dev

- Admin: `admin@kannondo.local` / `admin123`
- `DISABLE_AUTH=true` desactiva auth (testes)

## Próximos passos sugeridos

1. Migrar dados legados: `POST /admin/migrate-legacy` (após import Galileu)
2. Fase 3: PostgreSQL, CI/CD, exportação CSV
3. UX: toasts, edição avançada
