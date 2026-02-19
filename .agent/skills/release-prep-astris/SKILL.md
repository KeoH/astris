---
name: release-prep-astris
description: Prepares a new Astris release version by updating version metadata, changelog, release notes, and running local release checks. Use when asked to prepare versions like 0.1.x without publishing to package registries.
---

# Release Prep Skill for Astris

This skill standardizes how to prepare a new Astris release in this repository.

## When to use this skill

- A user asks to prepare a new version (for example: `Prepare 0.1.3`).
- Version metadata, documentation, and release notes must be aligned.
- The repository should be left release-ready locally.

## Out of scope

- Publishing to TestPyPI or PyPI.
- Creating git tags or GitHub releases unless explicitly requested.

## Project-specific constraints

- Keep changes minimal and explicit.
- Follow project conventions in `.github/copilot-instructions.md`.
- Keep docs, comments, and docstrings in English.
- Preserve existing behavior unless the user asks for semantic changes.

## Decision tree

1. **Scope confirmation**
   - If the user asks only for release prep, do not publish.
   - If the user asks for full release with publishing, follow `docs/internal/PUBLISHING.md` after prep.

2. **Version strategy**
   - Default to aligning all version surfaces in repo metadata and generated packaging artifacts when present.
   - If the user requests source-only changes, skip generated artifacts.

3. **Runtime version**
   - If `astris.__version__` exists, update it.
   - If it does not exist and user wants runtime version, add it in `astris/__init__.py`.

## Required execution steps

1. Read current version and target files:
   - `pyproject.toml`
   - `astris/__init__.py`
   - `CHANGELOG.md`
   - `docs/internal/releases/`
   - `README.md`
   - `docs/internal/PUBLISHING.md`
   - `Makefile`

2. Update version surfaces to the target version (for example `0.1.3`):
   - `pyproject.toml`
   - `astris/__init__.py` runtime version (if in scope)
   - `astris.egg-info/PKG-INFO` and `uv.lock` when requested/expected

3. Add release documentation:
   - New top entry in `CHANGELOG.md` with date and sections (`Added`, `Changed`, `Fixed` as applicable)
   - New file `docs/internal/releases/<VERSION>.md` using the internal template

4. Align public/internal docs if impacted:
   - `README.md`
   - `docs/user/*`
   - `docs/internal/*` (only relevant sections)

5. Run local validation:
   - `uv sync --group dev`
   - `uv run --group dev pytest`
   - `uv run --group dev pyright`
   - `make release-check`

6. Summarize outcomes:
   - Files changed
   - Checks executed and results
   - Any follow-up needed

## Validation notes

- Prefer project commands from `Makefile` and documented workflows.
- Do not fix unrelated failing tests unless requested.
- If unrelated checks fail, report clearly and keep release-prep changes isolated.

## Output expectations

When finishing a release prep task:

- Report exactly what was changed.
- List command results for validation.
- State that publishing is not included unless requested.
