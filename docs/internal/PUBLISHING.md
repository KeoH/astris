# Publishing Astris to PyPI

This guide describes the recommended workflow to publish new Astris releases to TestPyPI and PyPI.

## Requirements

- Have maintainer permissions for the project on PyPI.
- Have `uv` installed.
- Set environment variables with API tokens:

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=<pypi-token>
```

Use the TestPyPI token for TestPyPI.
Use the PyPI token for PyPI.

## 1) Prepare the version

Update the version and changelog before publishing:

- Bump `version` in `pyproject.toml`.
- Update `CHANGELOG.md` with the new entry.
- Add or update release notes in `docs/internal/releases/<VERSION>.md` for the GitHub release body.
- Verify that `README.md` and package metadata are still correct.

## 2) Run local checks

Use the built-in check command:

```bash
make release-check
```

This command runs:

- Development dependency sync.
- Tests (`pytest`).
- Artifact build (`sdist` and `wheel`).
- Metadata/render validation with `twine check`.

## 3) Publish to TestPyPI first

```bash
uv run --group dev python -m twine upload --repository testpypi dist/*.whl dist/*.tar.gz
```

Validate installation from TestPyPI in a clean environment:

```bash
python -m venv /tmp/astris-smoke
source /tmp/astris-smoke/bin/activate
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple astris==<VERSION>
python -c "import astris; print(astris.__all__)"
uvx astris new demo_site
```

## 4) Publish to PyPI

Once TestPyPI is validated:

```bash
uv run --group dev python -m twine upload dist/*.whl dist/*.tar.gz
```

## 5) Post-release verification

Verify public installation:

```bash
python -m venv /tmp/astris-prod-check
source /tmp/astris-prod-check/bin/activate
pip install astris==<VERSION>
python -c "from astris import Astris; print(Astris)"
uvx astris new hello_astris
```

Publish the matching GitHub release using the content from `docs/internal/releases/<VERSION>.md`.

## Common issues

- `twine check` fails because of HTML files in `dist/`:
  - Use only `dist/*.whl` and `dist/*.tar.gz`.
- The `astris` command does not appear in the global shell:
  - Use the active virtual environment binary or reinstall with `uv pip install -e .`.
- Error due to an existing version:
  - Bump `version` in `pyproject.toml` and build again.

## Release notes template

Create `docs/internal/releases/<VERSION>.md` with the following structure:

```markdown
# Astris <VERSION>

Release date: <YYYY-MM-DD>

## Highlights

<Short summary of the release focus>

## What's changed

### Added
- <Item>

### Changed
- <Item>

### Fixed
- <Item>

## Why this matters

- <User impact>

## Validation

- `uv run --group dev pyright` -> `<result>`
- `uv run --group dev pytest` -> `<result>`

## Upgrade notes

<Migration steps or "No migration is required.">
```
