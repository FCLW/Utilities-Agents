.PHONY: help dev test test-live build web deploy-portal deploy-fleet

help:
	@echo "Available commands:"
	@echo "  make dev            - Run agents locally with agents-cli dev"
	@echo "  make test           - Run agent unit and integration tests"
	@echo "  make test-live      - Run live evaluation across deployed Reasoning Engines"
	@echo "  make build          - Recompile web catalog.json and web portal index.html"
	@echo "  make web            - Build and launch local web portal at http://localhost:8000"
	@echo "  make deploy-portal  - Build and deploy web showcase portal to Cloud Run"
	@echo "  make deploy-fleet   - Deploy all 113 agents to Vertex AI Reasoning Engine"

VENV ?= .venv
PYTHON := $(VENV)/bin/python
ADK := $(VENV)/bin/adk
PYTEST := $(VENV)/bin/pytest

setup:
	@echo "Setting up local environment in $(VENV)..."
	uv pip install --default-index https://pypi.org/simple --python $(PYTHON) -e .

dev:
	$(ADK) api_server agents/

test:
	$(PYTEST) tests/

test-live:
	$(PYTHON) scripts/live_agent_portfolio_tester.py

build:
	$(PYTHON) scripts/build_catalog_json.py
	$(PYTHON) scripts/generate_web_portal.py

web: build
	$(PYTHON) -m http.server -d web 8000

deploy-portal: build
	$(PYTHON) scripts/deploy_web_portal.py

deploy-fleet:
	$(PYTHON) scripts/deploy_all_and_register.py

