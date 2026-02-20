# Astris Release Preparation Checklist

Use this checklist for version `<VERSION>`.

## Version alignment

- [ ] Update `pyproject.toml` version.
- [ ] Update `astris/__init__.py` runtime version (`__version__`) when in scope.
- [ ] Align generated metadata (`astris.egg-info/PKG-INFO`, `uv.lock`) when required.

## Release documentation

- [ ] Add new top entry in `CHANGELOG.md` with release date.
- [ ] Create `docs/internal/releases/<VERSION>.md`.
- [ ] Update `README.md` and `docs/user/*` if commands or behavior changed.

## Local validation

- [ ] `uv sync --group dev`
- [ ] `uv run --group dev pytest`
- [ ] `uv run --group dev pyright`
- [ ] `make release-check`

## Handoff

- [ ] Summarize changed files.
- [ ] Summarize check results.
- [ ] Confirm publishing is out of scope unless explicitly requested.
