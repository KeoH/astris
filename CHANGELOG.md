# Changelog

All notable changes to this project are documented in this file.

## [Unreleased]

### Changed
- Renamed the main application class from `AstrisApp` to `Astris`.

## [0.1.4] - 2026-02-21

### Added
- Added `astris deploy` CLI command with Cloudflare Pages support via `npx wrangler pages deploy`.
- Added project configuration support from `pyproject.toml` under `[tool.astris]`.
- Added environment variable injection from `[tool.astris.env]` for build/deploy workflows.
- Added public deployment guide at `docs/user/deployment.md`.

### Changed
- Updated package version metadata to `0.1.4`.
- Updated static build to optionally generate clean URLs (`route/index.html`) and extensionless internal links.
- Updated project scaffolding to generate a starter `pyproject.toml` with Astris configuration keys.
- Updated project scaffolding to be UV-first, removing generated `requirements.txt` and defining dependencies in `pyproject.toml`.

### Fixed
- Enabled extensionless route navigation for Cloudflare Pages deployments when clean URLs are enabled.

## [0.1.3] - 2026-02-20

### Added
- Added runtime version export as `astris.__version__` in the public API.
- Added workspace agent skill `release-prep-astris` under `.agent/skills/` to standardize release preparation workflows.
- Added reusable skill resources for release checklist and internal release note template.
- Added broad HTML wrapper coverage in `astris.lib` for the modern standard HTML tag set.
- Added English docstrings to HTML wrapper classes in `astris.lib`.
- Added JSON content collection helpers in `astris.content` with `register_json_collection(...)`.
- Added read-only development JSON endpoints per collection with configurable API prefixes.
- Added static detail-page generation from JSON entries using a Python template callable/class.

### Changed
- Updated package version metadata to `0.1.3`.
- Updated user-facing README with the new workspace skill usage section.
- Updated `Element.render()` to correctly render void HTML elements without closing tags.
- Updated user docs to include `astris.lib` API documentation and wrapper availability notes.
- Updated tests for expanded wrappers and void-element rendering behavior.
- Moved layout helpers (`Container`, `Column`, `Row`) to `astris.layout`.
- Updated public exports and docs to include JSON collection APIs.

## [0.1.2] - 2026-02-19

### Added
- Added `astris/py.typed` to mark the package as typed (PEP 561).
- Added head asset registration APIs in `AstrisApp`: `add_head_link(...)` and `add_head_script(...)`.
- Added user documentation site scaffolding with MkDocs in `docs/user/`.
- Added Read the Docs configuration via `.readthedocs.yml` and `mkdocs.yml`.
- Added documentation dependency group (`docs`) in `pyproject.toml` and RTD requirements file `docs/requirements-rtd.txt`.
- Added internal RTD operations guide at `docs/internal/RTD.md`.
- Added `make docs` and `make docs-serve` commands for local docs workflows.
- Added `astris build` CLI command to generate static output from `main.py` by default, with optional `--file` support.

### Changed
- Updated packaging configuration to include `py.typed` in distributed artifacts via `tool.setuptools.package-data`.
- Fixed consumer-side mypy warning: "Skipping analyzing \"astris\": module is installed, but missing library stubs or py.typed marker".
- Updated page rendering/build flow to inject registered CSS/JS assets into the document `<head>`.
- Updated `README.md` and `example.py` with CDN usage examples (Bootstrap).
- Separated documentation scope into `docs/user/` (public) and `docs/internal/` (maintainer-only).
- Moved publishing and release-note internal documentation under `docs/internal/`.
- Added a dedicated docs build job to `.github/workflows/tests.yml`.
- Updated `README.md` with user vs internal docs separation and local docs commands.
- Updated CLI docs and quickstart examples to use `astris build`, and aligned `make build` with `uv run astris build --file example.py`.

## [0.1.1] - 2026-02-18

### Added
- Added Pyright to the `dev` dependency group.
- Added Pyright configuration in `pyproject.toml`.
- Added a dedicated `typecheck` job to `.github/workflows/tests.yml`.

### Changed
- Updated `Element.__init__` typing for `children` to accept `Sequence[Component | str] | None`.
- Kept internal `children` storage materialized as `List[Component | str]` to preserve runtime behavior.

## [0.1.0] - 2026-02-18

### Added
- Renamed framework package to `astris`.
- Added installable CLI entrypoint: `astris`.
- Added `astris new <project_name>` scaffolding command.
- Added generated project template (`main.py`, `README.md`, `.gitignore`, `requirements.txt`).
- Added CLI test coverage in `tests/test_cli.py`.
- Added MIT license.

### Changed
- Updated project metadata for PyPI readiness in `pyproject.toml`.
- Updated Python requirement to `>=3.11`.
- Updated repository README with installation, usage, and release checklist.
