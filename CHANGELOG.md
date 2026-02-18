# Changelog

All notable changes to this project are documented in this file.

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
