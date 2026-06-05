# System Patterns

## Arquitetura

```
PDF (Galileu) → pdf_parser.py → Preview API → Confirmação → SQLite
                                                      ↓
                                            Frontend Dashboard (Next.js)
```

## Componentes

| Camada | Local | Responsabilidade |
|--------|-------|------------------|
| API | `backend/app/main.py` | Rotas FastAPI, upload, preview, confirmação, listagem |
| Parser | `backend/app/pdf_parser.py` | Extração regex/pdfplumber do Galileu |
| Modelos | `backend/app/models.py` | Aluno, Mensalidade (SQLAlchemy) |
| Schemas | `backend/app/schemas.py` | Validação Pydantic |
| DB | `backend/app/database.py` | Engine SQLite, sessões |
| UI | `frontend/src/app/` | Dashboard, upload, modal preview, detalhes aluno |

## Padrões de design

- **Upload em duas etapas**: preview sem side-effects, confirmação com persistência
- **Comparação por matrícula/dependente**: evita duplicidade de alunos
- **Docker Compose**: backend e frontend orquestrados; volumes para hot-reload
- **Makefile**: comandos padronizados (`dev`, `test`, `clean`, `logs`)

## Rotas principais (backend)

- `GET /` — health check
- `POST /upload-pdf-preview/` — parse + diff sem gravar
- `POST /upload-pdf-confirm/` — persiste dados aprovados
- `GET /alunos/` — listagem
- `GET /alunos/{id}` — detalhes com mensalidades
- `GET /metrics/` — métricas do dashboard

## Frontend

- App Router (Next.js 16)
- Página principal: `frontend/src/app/page.tsx`
- Detalhes do aluno: `frontend/src/app/alunos/[id]/page.tsx`
- Consome API via `FASTAPI_URL` (Docker) ou `http://localhost:8000`
