# Read the Docs Operations Guide

This document is for Astris maintainers.

It explains how to publish and update the user documentation hosted on Read the Docs (RTD).

## Documentation scope

- Public user docs source: `docs/user/`
- Internal maintainer docs source: `docs/internal/`

RTD must only publish the content from `docs/user/`.

## Relevant project files

- RTD config: `.readthedocs.yml`
- MkDocs config: `mkdocs.yml`
- RTD docs dependencies: `docs/requirements-rtd.txt`

## Local workflow before pushing

1. Sync docs dependencies:

```bash
uv sync --group docs
```

2. Run strict docs build:

```bash
make docs
```

3. Optional local preview with live reload:

```bash
make docs-serve
```

## First-time RTD setup

1. In Read the Docs, import the GitHub repository.
2. Confirm RTD detects `.readthedocs.yml` in the repository root.
3. Ensure the default branch is selected as the `latest` version.
4. Trigger the first build from the RTD project dashboard.

If build settings in the RTD UI conflict with `.readthedocs.yml`, prefer the repository configuration and remove conflicting UI overrides.

## Updating documentation

1. Edit public pages in `docs/user/`.
2. Validate locally with `make docs`.
3. Open and merge a pull request to `main`.
4. RTD should automatically rebuild `latest` after merge.

## Troubleshooting

### RTD build fails because dependencies are missing

- Verify required packages in `docs/requirements-rtd.txt`.
- Verify docs dependencies in `pyproject.toml` under the `docs` group.

### RTD publishes internal documentation

- Verify `mkdocs.yml` uses:

```yaml
docs_dir: docs/user
```

- Verify no navigation entries point to `docs/internal` content.

### Local docs build passes but RTD fails

- Re-check `.readthedocs.yml` Python version and install steps.
- Re-run local strict build with `make docs`.
- Compare RTD logs with local output.

## Operational rule

Treat `docs/user/` as the only publishable documentation source for RTD.
Keep internal process and release documentation in `docs/internal/` only.
