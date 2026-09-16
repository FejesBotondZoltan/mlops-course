.PHONY: up down down-v logs ps run test sync

## Bring up all four services and wait for healthchecks
up:
	docker compose up -d --wait

## Stop services (data persists in named volumes)
down:
	docker compose down

## Stop services AND wipe all volumes (fresh start)
down-v:
	docker compose down -v

## Stream logs from all services
logs:
	docker compose logs -f

## Show status of all services
ps:
	docker compose ps

## Run the pipeline (requires: stack up, uv sync)
run:
	uv run python src/main.py

## Run tests (no stack required)
test:
	uv run pytest tests/ -v

## Install Python dependencies
sync:
	uv sync --all-groups
