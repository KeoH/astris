# Changelog

All notable changes to this project are documented in this file.


## [0.1.5] - Unreleased

### Added
- Added modular route registration via `Router(prefix=...)` and `app.include_router(router)` to split page declarations across files.
- Added dynamic route support with path parameters (for example `/posts/{slug}`) for development runtime rendering.
- Added `static_params` in `page(...)` decorators to pre-generate dynamic routes during static `build()`.
- Added an extensible `Theme` API (`astris.theme.Theme`) with token groups for colors, spacing, custom scales, component defaults, and arbitrary extra metadata.
- Added built-in default theme preset factory `create_default_theme("light" | "dark")`.
- Added official soft preset factory `create_soft_theme("light" | "dark")` built on top of default theme tokens.
- Added typed style system in `astris.styles` (`Style`, enums, `EdgeInsets`, and variable-based `Theme`).
- Added reusable CSS orchestration via `astris.stylesheet.StyleSheet`.
- Added compatibility modules `astris.components` and `astris.core` (`AstrisApp` alias).
- Added predefined breakpoint support (`sm`, `md`, `lg`, `xl`, `2xl`) in `StyleSheet.add_breakpoint(...)`.
- Added convenience helpers for faster styling: `sx(...)`, `Style.merge(...)`, and `Theme.quick(...)`.
- Added typed `TextDecoration` helpers and enums in `astris.styles` to compose full `text-decoration` shorthand values (line/style/color/thickness), including multiple lines.
- Added external stylesheet registration in `astris.theme.Theme` via `stylesheets` and `add_stylesheet(...)`.
- Added `responsive` support in `StyleSheet.add_class(...)` to define class-level breakpoint overrides in the same call.
- Added `Style` support for class-local `states` and `selectors` so pseudo-states (`:hover`, `:focus-visible`) and structural selectors (`:nth-child(...)`, `& > ...`) can be defined without `add_raw(...)`.

### Changed
- Updated package version metadata to `0.1.5`.
- Prepared release documentation and internal release notes for `0.1.5`.
- Updated `example.py` to register pages through router modules and keep the entrypoint focused on app wiring.
- Updated public docs and README with router-based project organization guidance.
- Updated `Astris` to accept `theme=Theme(...)` and inject theme CSS variables into rendered pages.
- Updated `Astris()` to assign `create_default_theme()` automatically when no theme is provided.
- Updated page rendering to set `data-theme` and CSS `color-scheme` from theme mode (`light`/`dark`).
- Updated `Element` rendering to apply theme component defaults at render time with explicit attribute precedence.
- Updated layout helpers (`Column`, `Row`) to use spacing CSS variables by default.
- Updated public exports and user docs to include theme APIs.
- Updated public docs navigation with a dedicated `Styles` page (`docs/user/styles.md`) covering `astris.styles` usage examples.
- Reorganized public docs by moving theme guidance into dedicated page `docs/user/themes.md` and linking it from quickstart/home navigation.
- Expanded public docs with explicit media query guidance using `StyleSheet.add_media_query(...)`.
- Expanded public docs with a class-first guide for `Style` + `StyleSheet` (variants, breakpoints, raw selectors, and integration patterns).
- Updated `Theme` to own an optional `StyleSheet` (`set_stylesheet(...)`/`get_stylesheet(...)`) and inject class CSS automatically during page rendering.
- Renamed `GlobalStyleSheet` to `StyleSheet` and exported `StyleSheet` from the root public API.
- Updated head asset rendering order to inject theme external stylesheets before generated theme CSS and app-level head links.
- Updated link injection to deduplicate repeated stylesheet hrefs across theme and app-level head links.
- Updated `Theme` stylesheet validation to accept relative paths (for example `assets/site.css`) in addition to `https://...` and `/...`.
- Updated `run_dev()` to mount local `./assets` at `/assets` by default when the directory exists.
- Updated `build()` to copy local `./assets` into output and rewrite relative `assets/...` href values for nested routes.
- Updated `example.py` with a full theme-first walkthrough that connects app tokens, reusable CSS classes, and route composition.
- Updated public theme documentation (`docs/user/themes.md`) with a recommended step-by-step workflow aligned to `example.py`.
- Updated `README.md` theme section to point to the renewed example-driven workflow.

### Fixed
- Aligned release metadata across project files for consistent packaging and distribution workflows.
- Fixed `Element` style composition so `style=Style(...)` and `styles=[Style(...)]` are merged correctly without runtime errors.

## [0.1.4] - 2026-02-24

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
- Renamed the main application class from `AstrisApp` to `Astris`.

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
