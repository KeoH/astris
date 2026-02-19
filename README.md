# Astris

[![Tests](https://github.com/KeoH/astris/actions/workflows/tests.yml/badge.svg)](https://github.com/KeoH/astris/actions/workflows/tests.yml)

Astris is a minimal Python framework for building static websites using component-style APIs.

## Documentation

- User documentation (for building websites): `docs/user`
- Internal framework-maintainer documentation: `docs/internal`

## Installation

```bash
pip install astris
```

## Quick start with CLI

Create a new project scaffold:

```bash
uvx astris new my-project
cd my-project
uv run python main.py
```

Build static files:

```bash
uv run astris build
```

## Basic usage

```python
from astris import AstrisApp
from astris.lib import Body, H1, Html

app = AstrisApp()


@app.page("/")
def home():
	return Html(children=[
		Body(children=[
			H1(children=["Hello from Astris"]),
		])
	])


if __name__ == "__main__":
	app.run_dev()
```

## HTML tags API

`astris.lib` now provides wrappers for the modern standard HTML tag set (A to Z).
Each wrapper class includes an English docstring describing the underlying HTML element.

Void elements (for example `Img`, `Br`, `Input`, `Meta`) render without closing tags.

Layout helpers (`Container`, `Column`, `Row`) live in `astris.layout`.

```python
from astris.layout import Container, Column, Row
```

## Head assets (CDN)

You can register external CSS and JavaScript files that Astris injects into the page `<head>`.
This works in both `run_dev()` and `build()` outputs.

```python
from astris import AstrisApp

app = AstrisApp()

app.add_head_link(
	"https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
)
app.add_head_script(
	"https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
)
```

## Development

```bash
uv sync --group dev
uv pip install -e .
uv run --group dev pytest
```

## Documentation (local)

Build user documentation in strict mode:

```bash
make docs
```

Serve user documentation with live reload:

```bash
make docs-serve
```

## Continuous Integration

GitHub Actions runs tests on push and pull request events targeting main using Python 3.11, 3.12, and 3.13.
The workflow is defined in `.github/workflows/tests.yml`.

## Release checklist

```bash
make release-check
```

Equivalent manual commands:

```bash
uv sync --group dev
uv run --group dev pytest
uv run --group dev python -m build
uv run --group dev twine check dist/*.whl dist/*.tar.gz
```

`example.py` in this repository is an internal framework demo and not the standard end-user workflow.

## Agent skill: release-prep-astris

This repository includes a workspace skill at `.agent/skills/release-prep-astris`.

Use this skill when preparing a new Astris version and you want a repeatable release-prep workflow that covers:

- Version alignment across project metadata.
- Changelog and internal release notes updates.
- Local validation checks (`pytest`, `pyright`, `release-check`).

By default, this skill prepares the repository for release but does not publish artifacts to TestPyPI or PyPI unless explicitly requested.
