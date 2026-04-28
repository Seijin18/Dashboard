# 📋 Checklist de Desenvolvimento - Dashboard

Este documento serve como um guia para o desenvolvimento do projeto Dashboard. Ele detalha o que já foi implementado e o que ainda precisa ser feito para atingir os objetivos do projeto.

---

## 🟢 Fase 1: Core (Implementado)
Funcionalidades fundamentais que já estão operacionais.

### Backend (FastAPI & Parsing)
- [x] Configuração inicial do FastAPI (porta 8000).
- [x] Conexão com banco de dados SQLite via SQLAlchemy.
- [x] Modelagem de dados (`Aluno`, `Mensalidade`).
- [x] Parser de PDF (`pdfplumber`) otimizado para o sistema Galileu.
- [x] Rota de Preview (`/upload-pdf-preview/`) com lógica de comparação.
- [x] Rota de Confirmação (`/upload-pdf-confirm/`) para persistência de dados.
- [x] Lógica para evitar duplicidade de matrículas (identificação por dependente).
- [x] Suporte a CORS configurado.

### Frontend (Next.js)
- [x] Dashboard principal com cards de métricas (Total de Alunos, Ativos, Receita).
- [x] Componente de upload de PDF com validação.
- [x] Modal de pré-visualização de mudanças (Novos, Atualizados, Inalterados).
- [x] Tabela de listagem de alunos com status e badges.
- [x] Integração com API (Fetch/Refresh).
- [x] Estilização básica com Tailwind CSS.

### Infraestrutura
- [x] Dockerfile para Backend e Frontend.
- [x] `docker-compose.yml` para orquestração em desenvolvimento.

---

## 🟡 Fase 2: Próximos Passos (Curto Prazo)
Melhorias na experiência do usuário e robustez do sistema.

### Funcionalidades do Aluno
- [x] **Página de Detalhes:** Criar visualização individual para cada aluno.
- [x] **Histórico:** Exibir linha do tempo de mensalidades e status.
- [ ] **Edição Manual:** Permitir ajustes pontuais em dados de alunos sem depender de PDF.

### Interface & UX
- [x] **Filtros Avançados:** Filtrar tabela por Status, Nome, Contrato ou Data.
- [x] **Busca:** Campo de busca global para localizar alunos rapidamente.
- [x] **Gráficos:** Implementar componentes visuais (Recharts) para evolução da receita e distribuição de alunos.
- [ ] **Feedback Visual:** Toasts para notificações de sucesso/erro nos uploads.

### Qualidade de Código
- [ ] **Validação Pydantic:** Tornar os esquemas mais rigorosos.
- [x] **Logs:** Implementar sistema de logs no backend para monitorar o processamento de PDFs.
- [ ] **Testes:** Aumentar a cobertura de testes unitários no parser e nas rotas.

---

## 🔴 Fase 3: Maturidade (Longo Prazo/Produção)
Recursos necessários para um ambiente de produção seguro e escalável.

### Segurança
- [ ] **Autenticação:** Implementar login com JWT (JSON Web Tokens).
- [ ] **Autorização:** Níveis de acesso (Admin vs Consulta).
- [ ] **Proteção de Rotas:** Bloquear endpoints sensíveis.

### Gestão de Dados
- [ ] **Exportação:** Gerar relatórios em CSV/Excel/PDF.
- [ ] **Backups:** Sistema de backup automático do banco de dados.
- [ ] **Migrações (Alembic):** Configurar controle de versão do esquema do banco de dados.
- [ ] **Soft Delete:** Implementar exclusão lógica para preservação de dados históricos.

### DevOps & Escala
- [ ] **CI/CD:** Pipeline automatizada para rodar testes e build.
- [ ] **Otimização de Imagens:** Dockerfiles multi-stage para produção.
- [ ] **PostgreSQL:** Plano de migração do SQLite para PostgreSQL se a escala aumentar.
- [ ] **HTTPS/SSL:** Configuração de segurança de transporte.

---

## 📊 Status de Saúde do Projeto
| Categoria | Status | Nota |
| :--- | :--- | :--- |
| **Backend** | 🟢 Estável | Lógica de negócio core concluída. |
| **Frontend** | 🟡 Funcional | Precisa de filtros e visualizações detalhadas. |
| **Segurança** | 🔴 Inexistente | Prioridade para a Fase 3. |
| **DevOps** | 🟢 Configurado | Pronto para desenvolvimento local. |

---
*Última atualização: 27 de Abril de 2026*
