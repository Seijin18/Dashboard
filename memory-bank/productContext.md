# Product Context

## Problema

A gestão financeira da Kannon Do depende de relatórios exportados do sistema Galileu em PDF. Comparar manualmente o que mudou (novos alunos, pagamentos, pendências) é lento e propenso a erro.

## Solução

O Dashboard automatiza a leitura do PDF, detecta diferenças em relação ao banco local e permite confirmar apenas o que deve ser persistido — com visualização prévia em modal.

## Fluxo do usuário

1. Operador faz upload do PDF Galileu no dashboard
2. Sistema exibe preview: registros novos, atualizados e inalterados
3. Operador confirma a importação
4. Dashboard atualiza métricas (total de alunos, ativos, receita) e listagem
5. Operador pode abrir detalhes de um aluno para ver histórico de mensalidades

## Experiência desejada

- Interface moderna e responsiva (Next.js + Tailwind)
- Feedback visual claro no preview (badges de status)
- Operação segura: nada é gravado sem confirmação explícita
- Métricas financeiras visíveis na página principal

## Integrações

- **Entrada**: PDFs do Galileu (pasta `Reports/` para armazenamento local)
- **Saída**: SQLite local (`kannondo.db`) consumido pelo frontend via API FastAPI
