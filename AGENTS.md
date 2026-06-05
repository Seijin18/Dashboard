# Dashboard KannonDo — Guia para Agentes

## Contexto persistente

Este repositório usa duas camadas de memória para o agente:

1. **OpenSpec** (`openspec/`) — especificações, propostas de mudança e workflow spec-driven
2. **Memory Bank** (`memory-bank/`) — documentação viva do projeto entre sessões

### Início de cada sessão

1. Ler todos os arquivos em `memory-bank/`
2. Consultar `openspec/specs/` para requisitos vigentes
3. Verificar `CHECKLIST.md` para status de implementação

## OpenSpec (spec-driven development)

Comandos disponíveis no chat do Cursor (após reload):

| Comando | Uso |
|---------|-----|
| `/opsx:propose "ideia"` | Criar proposta de mudança com specs e tasks |
| `/opsx:explore` | Explorar o escopo antes de implementar |
| `/opsx:apply` | Implementar mudança aprovada |
| `/opsx:sync` | Sincronizar specs com o código |
| `/opsx:archive` | Arquivar mudança concluída |

Configuração do projeto: `openspec/config.yaml`

## Memory Bank

Comandos de workflow:

- `PLAN` — modo planejamento (sem alterar código)
- `ACT` — executar plano aprovado
- `update memory bank` — atualizar documentação após mudanças

Arquivos principais em `memory-bank/`:

- `projectbrief.md` — escopo e objetivos
- `productContext.md` — problema e experiência do usuário
- `systemPatterns.md` — arquitetura e padrões
- `techContext.md` — stack e setup de desenvolvimento
- `activeContext.md` — foco atual e próximos passos
- `progress.md` — status e histórico

## Comandos do projeto

```bash
make dev      # Docker: backend :8000, frontend :3001
make test     # pytest no backend
make logs     # logs dos containers
make clean    # para containers e apaga DB
```

Frontend nativo (Windows):

```powershell
cd frontend
npm install
npm run dev
```

## Regras de implementação

- Manter alterações focadas; não refatorar código não relacionado
- Backend: FastAPI + SQLAlchemy; rotas em `backend/app/main.py`
- Frontend: Next.js App Router em `frontend/src/app/`
- Parsing PDF: lógica em `backend/app/pdf_parser.py`, referência em `pdfExtract/`
- Após features significativas: atualizar memory-bank e, se aplicável, openspec specs
