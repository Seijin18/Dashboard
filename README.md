# Dashboard KannonDo

Bem-vindo ao repositório do **Dashboard KannonDo**, um sistema de ingestão, validação e visualização financeira desenhado para processar os relatórios extraídos nativamente do sistema **Galileu**. 

## 📌 Funcionalidades
- **Leitura Automática de PDF (pdfplumber)**: Um robô de parsing lê o modelo bruto do Galileu. Relaciona dependentes, datas de vencimento, status financeiro e contratos.
- **Pré-Visualização Inteligente (Modal)**: O Backend atua de formador de diferencial. Antes de submeter os dados para o banco, todos os registros são comparados com a base local para detectar faturas "**Novas**", "**Atualizadas**" (ex.: Pendente ➡️ Pago) e "**Inalteradas**".
- **Dashboard Front-end Responsivo**: Interface Tailwind v4/Next.js 16 para métricas globais e listagens.
- **Relatório de Atualizações**: Aviso com o número total de resumos inseridos, contadores e exibição comparativa na tela antes do commit no SQLite.

## 🛠 Arquitetura do Projeto
- **Backend**: Python 3.10+, FastAPI, SQLAlchemy, SQLite (banco leve, auto-contido: `kannondo.db`).
- **Frontend**: Next.js 16 (App Router), React, Tailwind CSS, Lucide-React.
- **Ambiente/Orquestração**: Docker & Docker Compose (para o ecossistema Python). No front-end indicamos a execução local no Windows (Node 20+) devido a restrições de permissões em volumes WSL durante o Live-Reloading do Turbopack.

## 🚀 Como Executar

### 1. Ambiente do Servidor (Backend em Docker)
Certifique-se de que possui o Docker e Docker Compose configurados no Windows Host.

Na raiz do repositório (`C:\Projetos\KannonDo\Dashboard`):
```bash
docker compose up -d backend
```
O Backend FastAPI e a documentação interativa Swagger estarão rodando em:
- API: `http://localhost:8000/`
- Docs: `http://localhost:8000/docs/`

### 2. Ambiente do Front-end (Next.js Nativo)
Vá até o diretório `frontend` e rode a instância local:

```powershell
cd frontend
npm install
npm run dev
```
O painel de métricas subirá na porta 3000 ou 3001 (se houver colisão de host):
- Web UI: `http://localhost:3001/`

### 🧪 Executando os Testes (Automáticos)
Escrevemos uma cobertura no framework **PyTest**. Esses testes usam `httpx` e o `TestClient` local da FastAPI para garantir que todos os nós do backend estão em harmonia.

Para rodar os testes da API diretamente no container instanciado:
```bash
docker exec -it kannondo-backend sh -c "pip install pytest httpx && pytest"
```

## 🏗 Estrutura das Pastas
- `/backend/app/main.py`: Entradas REST (Upload, Preview, Listagem).
- `/backend/app/models.py` & `schemas.py`: ORM para Tabela `alunos` e `mensalidades`.
- `/backend/app/pdf_parser.py`: Engine Regex de tratamento do Galileu.
- `/frontend/src/app/page.tsx`: Interface Global SPA Modal Dashboard.

---
Desenvolvido como extensão para o sistema integrado de dojo Kannon Do.