.PHONY: help build up down restart logs clean status proof proof-logs

PYTHON ?= .venv/bin/python

help:
	@echo "Targets: build up down restart logs clean status proof proof-logs"

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
test:
	$(PYTHON) -m pytest
test-mediasort:
	$(PYTHON) -m pytest -m mediasort --junitxml=test-results-mediasort.xml
test-makeproofs:
	$(PYTHON) -m pytest -m makeproofs --junitxml=test-results-makeproofs.xml
test-docker:
	$(PYTHON) -m pytest -m docker --junitxml=test-results-docker.xml