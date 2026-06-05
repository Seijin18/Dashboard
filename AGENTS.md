# Dashboard KannonDo — Agentes

## Contexto persistente

| Camada | Onde | Quando carregar |
|--------|------|-----------------|
| Memory Bank | `memory-bank/` | `activeContext.md` por padrão; resto sob demanda |
| OpenSpec | `openspec/` | Features multi-arquivo ou escopo incerto |
| Checklist | `CHECKLIST.md` | Planejamento de features |

## Comandos

**OpenSpec:** `/opsx:propose`, `/opsx:explore`, `/opsx:apply`, `/opsx:sync`, `/opsx:archive`

**Memory Bank:** `update memory bank` (atualiza `activeContext` + `progress`)

**Dev:** `make dev` · `make test` · `make clean` · `cd frontend && npm run dev`

## Eficiência

- Regras em `.cursor/rules/dashboard-agent.mdc` governam leitura seletiva e uso de tokens
- Bugs/ajustes pequenos: implementar direto, sem OpenSpec
- Detalhes de stack: `memory-bank/techContext.md` e `openspec/config.yaml`
