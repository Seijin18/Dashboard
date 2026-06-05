# Progress

## O que funciona (Fase 1 — concluída)

### Backend
- [x] FastAPI na porta 8000 com Swagger
- [x] SQLite + SQLAlchemy (Aluno, Mensalidade)
- [x] Parser PDF Galileu (`pdfplumber`)
- [x] Preview com diff (novos / atualizados / inalterados)
- [x] Confirmação e persistência
- [x] Anti-duplicidade por matrícula/dependente
- [x] CORS configurado
- [x] Testes pytest (`make test`)

### Frontend
- [x] Dashboard com métricas (alunos, ativos, receita)
- [x] Upload de PDF com validação
- [x] Modal de preview de mudanças
- [x] Tabela de alunos com badges de status
- [x] Página de detalhes do aluno (`/alunos/[id]`)
- [x] Histórico de mensalidades

### Infra
- [x] Docker Compose (backend + frontend)
- [x] Makefile com comandos padronizados

## Em andamento / configurado agora

- [x] OpenSpec (spec-driven workflow)
- [x] Memory Bank (contexto persistente entre sessões)
- [x] Codebase indexing otimizado (`.cursorignore`)

## Pendente (Fase 2+)

- [ ] Edição manual de dados de alunos
- [ ] Melhorias de UX e robustez (ver `CHECKLIST.md`)
- [ ] Ambiente de produção dedicado

## Problemas conhecidos

- Nenhum bloqueador crítico documentado no momento
- Parsing depende do formato específico do PDF Galileu

## Histórico recente

- **2026-06-05**: Configuração de OpenSpec + Memory Bank no repositório
