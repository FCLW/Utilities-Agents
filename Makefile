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

dev:
	agents-cli dev

test:
	pytest agents/

test-live:
	python3 scripts/live_agent_portfolio_tester.py

build:
	python3 scripts/build_catalog_json.py
	python3 scripts/generate_web_portal.py

web: build
	python3 -m http.server -d web 8000

deploy-portal: build
	python3 scripts/deploy_web_portal.py

deploy-fleet:
	python3 scripts/deploy_all_and_register.py
