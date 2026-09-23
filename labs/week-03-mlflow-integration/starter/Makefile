.PHONY: up down down-v logs ps sync run sweep best register promote trace all test test-fast

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

## Install Python dependencies
sync:
	uv sync --all-groups

## Exercises 1-2 — one fully-logged run (params, metrics, tags, plots, model)
run:
	uv run python src/main.py run

## Exercise 3 — parameter sweep: one parent run with six children
sweep:
	uv run python src/main.py sweep

## Exercise 4 — server-side search: find and print the best run
best:
	uv run python src/main.py best

## Exercise 5 — register the best run's model (creates a new version)
register:
	uv run python src/main.py register

## Exercise 6 — promote the newest version to @staging with governance tags
promote:
	uv run python src/main.py promote

## Exercise 6 — traceability check: alias -> version -> run -> params
trace:
	uv run python src/main.py trace

## Exercises 1-6 end to end
all:
	uv run python src/main.py all

## Run every test (live tests auto-skip when the stack is down)
test:
	uv run pytest tests/ -v

## Run only the tests that do not need the stack
test-fast:
	uv run pytest tests/ -v -m "not live"
