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

dev-rm:
	docker compose -p $(NAME)-dev -f $(DEV_FILE) down --rmi all -v

dev-restart: dev-rm dev-stop dev-build dev-start

dev-restart-service:
	docker compose -p $(NAME)-dev -f $(DEV_FILE) build --no-cache $(SERVICE)
	docker compose -p $(NAME)-dev -f $(DEV_FILE) restart $(SERVICE)

test-build:
	docker compose -p $(NAME)-test -f $(TEST_FILE) build --no-cache --build-arg TEST=true

test-start:
	docker compose -p $(NAME)-test -f $(TEST_FILE) up --abort-on-container-exit --exit-code-from api

test-stop:
	docker compose -p $(NAME)-test -f $(TEST_FILE) down -v

test-rm:
	docker compose -p $(NAME)-test -f $(TEST_FILE) down --rmi all -v

test-restart: test-stop test-rm test-build test-start

test: test-stop test-start

prod-build:
	docker compose -p $(NAME)-prod -f $(PROD_FILE) build --no-cache

prod-start:
	docker compose -p $(NAME)-prod -f $(PROD_FILE) up -d

prod-stop:
	docker compose -p $(NAME)-prod -f $(PROD_FILE) down

prod-rm:
	docker compose -p $(NAME)-prod -f $(PROD_FILE) down --rmi all -v

prod-restart: prod-stop prod-rm prod-build prod-start

pre-commit-install:
	uv tool install prek
	prek install

pre-commit-run:
	prek run --all-files

clean:
	docker system prune -f
