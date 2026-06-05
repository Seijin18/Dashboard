# Project Brief — Dashboard KannonDo

## Objetivo

Sistema de ingestão, validação e visualização financeira para a academia de artes marciais **Kannon Do**. Processa relatórios PDF exportados do sistema **Galileu**, compara com dados históricos e exibe métricas de mensalidades e alunos.

## Escopo principal

- Upload e parsing automático de PDFs financeiros (Galileu)
- Preview inteligente antes de persistir (Novos / Atualizados / Inalterados)
- Dashboard com métricas globais e listagem de alunos
- Página de detalhes por aluno com histórico de mensalidades
- API REST documentada via Swagger

## Fora de escopo (por ora)

- Edição manual de dados de alunos (planejado na Fase 2)
- Ambiente de produção dedicado (docker-compose.prod.yml)
- Autenticação e multi-tenant

## Stakeholders

- Gestão da academia Kannon Do (visualização financeira)
- Operadores que importam relatórios Galileu em PDF

## Critérios de sucesso

- Importação confiável de PDFs sem duplicar matrículas
- Preview claro das mudanças antes do commit no banco
- Dashboard responsivo com dados atualizados após importação
