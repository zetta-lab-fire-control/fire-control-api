NAME=uai-fire-control-api
DEV_FILE=deploy/compose/dev.yml
TEST_FILE=deploy/compose/test.yml
PROD_FILE=deploy/compose/prod.yml

dev-build:
	docker compose -p $(NAME)-dev -f $(DEV_FILE) build --no-cache

dev-start:
	docker compose -p $(NAME)-dev -f $(DEV_FILE) up -d

dev-stop:
	docker compose -p $(NAME)-dev -f $(DEV_FILE) down

dev-restart: dev-stop dev-build dev-start make clean

dev-restart-service:
	docker compose -p $(NAME)-dev -f $(DEV_FILE) build --no-cache $(SERVICE)
	docker compose -p $(NAME)-dev -f $(DEV_FILE) restart $(SERVICE)

dev-rm:
	docker compose -p $(NAME)-dev -f $(DEV_FILE) down --rmi all -v
	make clean

test-build:
	docker compose -p $(NAME)-test -f $(TEST_FILE) build --build-arg TEST=true

test-start:
	docker compose -p $(NAME)-test -f $(TEST_FILE) up --abort-on-container-exit --exit-code-from app-tests

test-rm:
	docker compose -p $(NAME)-test -f $(TEST_FILE) down --rmi all -v

prod-build:
	docker compose -p $(NAME)-prod -f $(PROD_FILE) build --no-cache

prod-start:
	docker compose -p $(NAME)-prod -f $(PROD_FILE) up -d

prod-stop:
	docker compose -p $(NAME)-prod -f $(PROD_FILE) down

prod-restart:
	prod-stop
	prod-build
	prod-start
	make clean

prod-rm:
	docker compose -p $(NAME)-prod -f $(PROD_FILE) down --rmi all -v
	make clean

pre-commit-install:
	uv tool install prek
	prek install

pre-commit-run:
	prek run --all-files

clean:
	docker system prune -f
