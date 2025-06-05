ENV_NAME = masc

# Запускает контейнеры с пересборкой и принудительным пересозданием, затем сразу выводит логи
up:
	@docker compose -f docker-compose.yml -p $(ENV_NAME) up --build -d --force-recreate
	@docker compose -f docker-compose.yml -p $(ENV_NAME) logs -f

# Запускает контейнеры в фоновом режиме без вывода логов и без пересборки
bg:
	@docker compose -f docker-compose.yml -p $(ENV_NAME) up -d

# Останавливает и удаляет все контейнеры, связанные с проектом $(ENV_NAME)
dn:
	@docker compose -f docker-compose.yml -p $(ENV_NAME) down

# Останавливает и удаляет контейнеры, а также удаляет все тома, связанные с проектом $(ENV_NAME)
cv:
	@docker compose -f docker-compose.yml -p $(ENV_NAME) down --volumes

# Останавливает и удаляет контейнеры, образы, тома и сети, связанные только с проектом $(ENV_NAME),
# а также удаляет висячие контейнеры и образы, которые не используются другими контейнерами
cp:
	@docker compose -f docker-compose.yml -p $(ENV_NAME) down --volumes --rmi all --remove-orphans

# Полная очистка всех ресурсов Docker:
# - Останавливает и удаляет все контейнеры, образы, тома и сети
# - Удаляет висячие контейнеры и образы, не используемые другими контейнерами
# - Удаляет все тома, все образы и все сети, не используемые другими контейнерами
# - Очищает Docker-систему от всех ненужных файлов и данных
ca:
	@docker compose down --volumes --rmi all --remove-orphans || true
	@docker rm -f $$(docker ps -aq) || true
	@docker rmi -f $$(docker images -aq) || true
	@docker volume rm -f $$(docker volume ls -q) || true
	@docker network rm $$(docker network ls -q) || true
	@docker system prune -a --volumes -f
	@docker builder prune -a -f

# Копирует файл переменных окружения из .env.example в .env
en:
	cp .env.example .env