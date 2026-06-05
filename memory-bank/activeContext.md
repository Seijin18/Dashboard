# Active Context

## Foco atual

Configuração inicial de **OpenSpec** e **Memory Bank** no repositório Dashboard para desenvolvimento assistido por IA com contexto persistente.

## Configuração recém-aplicada

- `openspec init --tools cursor` — skills e comandos OPSX em `.cursor/`
- `openspec/config.yaml` — contexto do projeto KannonDo
- `npx cursor-bank init` — regras de memory bank em `.cursor/rules/`
- `memory-bank/` — documentação inicial populada
- `AGENTS.md` — guia de workflow para agentes
- `.cursorignore` — otimização do codebase indexing

## Próximos passos sugeridos

1. Recarregar o Cursor (`Developer: Reload Window`) para ativar comandos `/opsx:*`
2. Abrir o projeto `C:\Users\marco\Projects\Dashboard` no Cursor
3. Continuar Fase 2 do `CHECKLIST.md`:
   - Edição manual de dados de alunos
   - Melhorias de UX e robustez pendentes

## Decisões em vigor

- Usar **clangd/OpenSpec + Memory Bank** em vez de depender só do chat
- Manter documentação em português (BR)
- Workflow: PLAN → ACT para mudanças; `update memory bank` após features

## Referências rápidas

- Status de features: `CHECKLIST.md`
- Regras Next.js: `frontend/AGENTS.md`
- Parsing Galileu: `pdfExtract/` e `backend/app/pdf_parser.py`
