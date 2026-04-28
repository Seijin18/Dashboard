# Dashboard KannonDo

Bem-vindo ao repositório do **Dashboard KannonDo**, um sistema de ingestão, validação e visualização financeira desenhado para processar os relatórios extraídos nativamente do sistema **Galileu**. O projeto automatiza a leitura de PDF, comparação de dados históricos e acompanhamento de pagamentos para a academia de artes marciais Kannon Do.

## 📌 Funcionalidades
- **Leitura Automática de PDF (pdfplumber)**: Um robô de parsing lê o modelo bruto do Galileu. Relaciona dependentes, datas de vencimento, status financeiro e contratos.
- **Pré-Visualização Inteligente (Modal)**: O Backend atua como formador de diferencial. Antes de submeter os dados para o banco, todos os registros são comparados com a base local para detectar faturas "**Novas**", "**Atualizadas**" (ex.: Pendente ➡️ Pago) e "**Inalteradas**".
- **Dashboard Front-end Responsivo**: Interface moderna (App Router) para métricas globais e listagens de mensalidades.
- **Relatório de Atualizações**: Aviso com o número total de resumos inseridos, contadores e exibição comparativa na tela antes do commit no SQLite.

## 🛠 Arquitetura & Tecnologias
- **Backend**: Python 3.10+, FastAPI, SQLAlchemy, SQLite (banco leve, auto-contido: `kannondo.db`).
- **Frontend**: Next.js 16 (App Router), React 19, Tailwind CSS v4, Lucide-React.
- **Orquestração**: Docker & Docker Compose para o ecossistema backend.
- **Parsing**: `pdfplumber` com lógica regex para extração precisa de tabelas financeiras.

## 🚀 Como Executar

O projeto utiliza um `Makefile` para facilitar os comandos comuns.

### 1. Iniciar Ambiente Completo (Recomendado)
Para subir o backend em Docker e preparar o ambiente:
```bash
make dev
```
- API/Swagger Docs: `http://localhost:8000/docs`
- Web Interface: `http://localhost:3000` ou `http://localhost:3001`

### 2. Execução Manual do Frontend
Se preferir rodar o frontend nativamente no Windows (para melhor performance de Hot Reload):
```powershell
cd frontend
npm install
npm run dev
```

### 🧪 Executando os Testes
A suíte de testes utiliza **PyTest** e garante a integridade das rotas de upload e listagem:
```bash
make test
```

## 🏗 Estrutura das Pastas
- `/backend`: Servidor FastAPI com lógica de negócio e banco de dados.
- `/frontend`: Aplicação Next.js/React.
- `/pdfExtract`: Documentação de referência, schema e regras de parsing para o sistema Galileu.
- `/Reports`: Pasta para armazenamento dos relatórios PDF originais.

## 🛠 Comandos úteis (Makefile)
- `make logs`: Acompanha a saída dos containers em tempo real.
- `make bash-backend`: Acessa o shell do container do backend.
- `make clean`: Para os containers e remove volumes (limpa o banco de dados).

- `/backend/app/pdf_parser.py`: Engine Regex de tratamento do Galileu.
- `/frontend/src/app/page.tsx`: Interface Global SPA Modal Dashboard.

---
Desenvolvido como extensão para o sistema integrado de dojo Kannon Do.