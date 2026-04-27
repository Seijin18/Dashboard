.PHONY: dev prod test clean build bash-backend logs

# Comandos base do Docker
DOCKER_COMPOSE = docker compose

# Levanta o ambiente de desenvolvimento (ambos backend e frontend)
dev:
	@echo "Iniciando ambiente de desenvolvimento (Docker)..."
	$(DOCKER_COMPOSE) up --build -d
	@echo "-> Frontend: http://localhost:3000 (ou 3001 em caso de conflito)"
	@echo "-> Backend: http://localhost:8000"

# Levanta o ambiente simulando produção
prod:
	@echo "Iniciando ambiente de producao (Docker)..."
	# Pode ser expandido para usar um docker-compose.prod.yml futuramente
	$(DOCKER_COMPOSE) up --build -d

# Executa a suíte de testes no backend (PyTest)
test:
	@echo "Rodando testes automatizados no backend..."
	docker exec kannondo-backend sh -c "PYTHONPATH=/app pytest tests/ -v"

# Acompanhar os logs do backend e frontend ao vivo
logs:
	$(DOCKER_COMPOSE) logs -f

# Entra no terminal do container do backend (útil para debug local)
bash-backend:
	docker exec -it kannondo-backend bash

# Desliga os containers, clean up de volumes (Reset do Banco de Dados) e caches
clean:
	@echo "Parando containers e removendo volumes do Docker..."
	$(DOCKER_COMPOSE) down -v
	@echo "Containers parados."
