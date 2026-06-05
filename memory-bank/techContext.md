# Tech Context

## Stack

| Camada | Tecnologia | Versão |
|--------|-----------|--------|
| Backend | Python, FastAPI, SQLAlchemy | 3.10+ |
| Banco | SQLite | `kannondo.db` |
| Parsing | pdfplumber + regex | — |
| Frontend | Next.js, React, Tailwind | 16 / 19 / v4 |
| Gráficos | Recharts | 2.x |
| Ícones | Lucide React | — |
| Testes | pytest | backend/tests/ |
| Containers | Docker Compose | backend + frontend |

## Setup de desenvolvimento

### Docker (recomendado)

```bash
make dev
```

- Backend: http://localhost:8000 (Swagger em /docs)
- Frontend: http://localhost:3001

### Frontend nativo (Windows)

```powershell
cd frontend
npm install
npm run dev
```

### Testes

```bash
make test
```

Roda pytest dentro do container `kannondo-backend`.

## Variáveis de ambiente

- `FASTAPI_URL` — URL do backend (frontend em Docker usa `http://backend:8000`)
- `WATCHFILES_FORCE_POLLING=true` — hot-reload no backend em volume Docker

## Dependências notáveis

- `backend/requirements.txt` — FastAPI, SQLAlchemy, pdfplumber, pytest
- `frontend/package.json` — Next.js 16, React 19, Tailwind v4

## Restrições

- Banco SQLite local (sem PostgreSQL em produção ainda)
- CORS aberto em desenvolvimento
- Parsing acoplado ao formato de PDF do Galileu (ver `pdfExtract/`)

## Ferramentas de agente configuradas

- **OpenSpec**: `openspec/`, comandos `/opsx:*` no Cursor
- **Memory Bank**: `memory-bank/`, regras em `.cursor/rules/`
- **Codebase indexing**: `.cursorignore` exclui node_modules, .next, logs, PDFs e DB
