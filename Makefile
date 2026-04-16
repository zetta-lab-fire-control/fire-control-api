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

test:
	docker compose -p $(NAME)-test -f $(TEST_FILE) run --rm api pytest --cov=/api --cov-report=term-missing --cov-report=markdown:/tests/coverage.md /tests -x -v

test-rm:
	docker compose -p $(NAME)-test -f $(TEST_FILE) down --rmi all -v

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

create-release:
	gh release create $(VERSION) --title "Release $(VERSION)" --notes "Release of version $(VERSION) of the api. $(RELEASE_NOTES)"
