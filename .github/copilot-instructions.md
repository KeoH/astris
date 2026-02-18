# Copilot Instructions for `astris`

## Big picture architecture
- Core package is `astris/` only. Do not reintroduce legacy `src/` or `main.py`.
- Public API is exported from `astris/__init__.py` (`AstrisApp`, `Component`, `Element`, `Text`).
- App lifecycle lives in `astris/app.py`:
  - `@app.page("/route")` registers routes and stores a rendered component tree in `self.routes`.
  - `run_dev()` serves via FastAPI/Uvicorn and supports reload via import string inference.
  - `build()` writes static HTML files to `dist/` and rewrites internal route links.
- Component system is simple string rendering:
  - `astris/component.py`: `Component` (abstract), `Text`, `Element`.
  - `astris/lib.py`: HTML tag wrappers + layout helpers (`Container`, `Column`, `Row`).

## Critical behavior to preserve
- `page()` currently evaluates page functions at decoration time; keep this behavior unless explicitly changing framework semantics.
- Attribute normalization in `Element` is required (`class_name` -> `class`, `_` -> `-`).
- Static build must preserve `<!DOCTYPE html>` and convert internal `href` routes to relative `.html` links.
- `run_dev(reload=True)` depends on an entrypoint-level variable named `app` (see `example.py`) to build `"<module>:app._fastapi_app"`.

## Dev workflows (use these commands)
- Dependency sync (including test tools): `uv sync --group dev`
- Editable install: `uv pip install -e .`
- Run tests: `uv run --group dev pytest`
- Coverage: `uv run --group dev pytest --cov=astris --cov-report=term-missing --cov-report=html`
- Run dev server: `uv run python example.py`
- Build static site: `uv run python example.py build`
- Equivalent shortcuts are in `Makefile` (`make sync`, `make test`, `make dev`, `make build`).

## Testing conventions in this repo
- Test framework is `pytest` with config in `pyproject.toml` (`testpaths = ["tests"]`, `addopts = "-q"`).
- Follow current structure:
  - `tests/test_component.py` for rendering primitives.
  - `tests/test_lib.py` for tag wrappers/layout helpers.
  - `tests/test_app_core.py` for routing/import-string helpers.
  - `tests/test_build.py` for static output + link rewriting.
  - `tests/test_run_dev.py` for uvicorn invocation behavior.
- For `run_dev` tests, monkeypatch `astris.app.uvicorn.run`; do not boot real servers.
- For build tests, use `tmp_path` and assert generated files/content directly.

## Project-specific coding patterns
- Keep implementation minimal and explicit; avoid introducing heavy abstractions.
- Prefer extending `Element` for new HTML-like components.
- Keep internal link rewriting logic centralized in `AstrisApp._rewrite_static_links`.
- If adding CLI/entrypoints, preserve compatibility with existing `example.py` workflow unless asked otherwise.
- Write all new/updated documentation in English.
- Write all new/updated code comments and docstrings in English.

## Typing guardrail for `children`
- `Element.__init__` accepts `children` as `Sequence[Component | str] | None`.
- Keep the internal representation as `List[Component | str]` (materialize with `list(children)` when provided).
- Reason: avoid `list` invariance issues in Pyright/Pylance for patterns like `children=[Div(...)]`.
- Do not revert to `List[Component | str]` in the input parameter unless typing behavior is intentionally changed.

## Type checking workflow
- Pyright is part of the `dev` dependency group.
- Local type check command: `uv run --group dev pyright`.
- CI includes a dedicated `typecheck` job in `.github/workflows/tests.yml`.
