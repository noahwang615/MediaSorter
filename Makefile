.PHONY: help build up down restart logs clean status proof migrate migrate-apply

help:
	@echo "Targets: build up down restart logs clean status proof migrate migrate-apply"

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

restart: down up

logs:
	docker compose logs -f

status:
	docker compose ps

proof:
	docker compose run --rm --build --entrypoint python mediasorter scripts/make_proofs.py

proof-logs:
	docker compose logs -f make_proofs

clean: down
	docker image rm mediasorter:latest 2>/dev/null || true
