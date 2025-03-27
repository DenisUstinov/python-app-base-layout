APP = src
COMPOSE_FILE = -f docker-compose.$(APP).yml
PROJECT_NAME = -p $(APP)

up:
	@docker compose $(COMPOSE_FILE) $(PROJECT_NAME) up --build -d --force-recreate
	@docker compose $(COMPOSE_FILE) $(PROJECT_NAME) logs -f

bg:
	@docker compose $(COMPOSE_FILE) $(PROJECT_NAME) up -d

dn:
	@docker compose $(COMPOSE_FILE) $(PROJECT_NAME) down

cl:
	@docker compose $(COMPOSE_FILE) $(PROJECT_NAME) down --volumes --rmi all --remove-orphans