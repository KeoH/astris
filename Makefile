.PHONY: help sync install test test-cov ruff ruff-check dev build docs docs-serve release-check release-upload

help:
	@echo "Available commands:"
	@echo "  make sync       - Sync dependencies (including dev)"
	@echo "  make install    - Install package in editable mode"
	@echo "  make test       - Run tests"
	@echo "  make test-cov   - Run tests with coverage"
	@echo "  make ruff       - Apply Ruff lint fixes and format code"
	@echo "  make ruff-check - Validate lint and formatting without modifying files"
	@echo "  make dev        - Start development server"
	@echo "  make build      - Generate static site in dist/"
	@echo "  make docs       - Build user docs with MkDocs (strict)"
	@echo "  make docs-serve - Serve user docs locally with live reload on port 9000"
	@echo "  make release-check - Run pre-release checks for PyPI publishing"
	@echo "  make release-upload - Upload built artifacts to PyPI"

sync:
	uv sync --group dev

install:
	uv pip install -e .

test:
	uv run --group dev python -m pytest

test-cov:
	uv run --group dev python -m pytest --cov=astris --cov-report=term-missing --cov-report=html

ruff:
	uvx ruff check --fix .
	uvx ruff format .

ruff-check:
	uvx ruff check .
	uvx ruff format --check .

dev:
	uv run python example.py

build:
	uv run astris build --file example.py

docs:
	uv run --group docs mkdocs build --strict

docs-serve:
	uv run --group docs mkdocs serve -a 127.0.0.1:9000

release-check:
	uv sync --group dev
	uv run --group dev python -m pytest --cov=astris --cov-report=term-missing
	uv run --group dev python -m build
	uv run --group dev python -m twine check dist/*.whl dist/*.tar.gz

release-upload:
	@test -f .env || (echo "Missing .env file with TWINE credentials"; exit 1)
	@set -a; . ./.env; set +a; \
		test -n "$$TWINE_USERNAME" || (echo "TWINE_USERNAME is not set"; exit 1); \
		test -n "$$TWINE_PASSWORD" || (echo "TWINE_PASSWORD is not set"; exit 1); \
		uv run --group dev python -m twine upload --repository pypi dist/*.whl dist/*.tar.gz
