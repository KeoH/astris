.PHONY: help sync install test test-cov ruff ruff-check dev build release-check

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
	@echo "  make release-check - Run pre-release checks for PyPI publishing"

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
	uv run python example.py build

release-check:
	uv sync --group dev
	uv run --group dev python -m pytest
	uv run --group dev python -m build
	uv run --group dev python -m twine check dist/*.whl dist/*.tar.gz
