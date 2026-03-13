from __future__ import annotations

import argparse
import importlib.util
import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Any

from . import __version__ as ASTRIS_VERSION
from .app import Astris

MAIN_TEMPLATE = """import sys

from astris import Astris
from astris.lib import Div, H1, P
from astris.themes.default import theme
from astris.themes.default.components import Badge, Btn, SimpleCard, SiteHeader, SiteNavbar
from astris.themes.default.layout import astris_ui_layout

app = Astris(theme=theme)


@app.page("/")
def home():
    navbar = SiteNavbar(
        options=[
            {"label": "Home", "href": "/", "active": True},
            {"label": "Documentation", "href": "https://astris.readthedocs.io"},
            {"label": "GitHub", "href": "https://github.com/keoh/astris"},
        ]
    )

    return astris_ui_layout(
        content=[
            SiteHeader("Astris", navbar),
            Div(
                class_name="container section stack-md",
                children=[
                    Badge("DEFAULT THEME", variant="primary"),
                    H1("Welcome to your new Astris project"),
                    P(
                        "This starter project uses the bundled default theme, layout helper, and reusable components."
                    ),
                    Div(
                        class_name="row",
                        children=[
                            Div(
                                class_name="col-12 col-md-6",
                                children=[
                                    SimpleCard(
                                        title="Fast start",
                                        content="Edit this page and compose new routes with themed components.",
                                    )
                                ],
                            ),
                            Div(
                                class_name="col-12 col-md-6",
                                children=[
                                    SimpleCard(
                                        title="Build ready",
                                        content="Run astris build to generate static HTML from your routes.",
                                    )
                                ],
                            ),
                        ],
                    ),
                    Div(
                        class_name="d-flex gap-4",
                        children=[
                            Btn("Read Docs", variant="primary", onclick="location.href='https://astris.readthedocs.io'"),
                            Btn("View API", variant="secondary", onclick="location.href='https://astris.readthedocs.io/en/latest/api/'"),
                        ],
                    ),
                ],
            ),
        ]
    )


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        app.build()
    else:
        app.run_dev(reload=True)

"""

README_TEMPLATE = """# {project_name}

Project generated with `astris new`.

## Install dependencies (uv)

```bash
uv sync
```

## Run in development

```bash
uv run python main.py
```

## Build static site

```bash
uv run astris build
```
"""

GITIGNORE_TEMPLATE = """__pycache__/
*.pyc
.venv/
dist/
"""

PYPROJECT_TEMPLATE = """[project]
name = "{project_name}"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "astris=={astris_version}",
]

[tool.astris]

[tool.astris.build]
output_dir = "dist"
clean_urls = false

[tool.astris.deploy]
provider = "cloudflare"

[tool.astris.deploy.cloudflare]
project_name = "replace-with-your-cloudflare-project-name"

[tool.astris.env]
# EXAMPLE_API_URL = "https://api.example.com"
"""


class CliError(ValueError):
    """CLI usage error for project generation."""


def validate_project_name(project_name: str) -> None:
    """Validate that the provided project name is filesystem friendly."""
    pattern = r"^[A-Za-z][A-Za-z0-9_-]*$"
    if not re.match(pattern, project_name):
        raise CliError(
            "Invalid project name. Use letters, numbers, '_' or '-', and start with a letter."
        )


def create_project(project_name: str, base_path: Path | None = None) -> Path:
    """Create a minimal Astris project scaffold."""
    validate_project_name(project_name)

    root = (base_path or Path.cwd()) / project_name
    if root.exists():
        raise CliError(f"Target directory already exists: {root}")

    root.mkdir(parents=True, exist_ok=False)

    (root / "main.py").write_text(MAIN_TEMPLATE, encoding="utf-8")
    (root / "README.md").write_text(
        README_TEMPLATE.format(project_name=project_name), encoding="utf-8"
    )
    (root / ".gitignore").write_text(GITIGNORE_TEMPLATE, encoding="utf-8")
    (root / "pyproject.toml").write_text(
        PYPROJECT_TEMPLATE.format(
            project_name=project_name,
            astris_version=ASTRIS_VERSION,
        ),
        encoding="utf-8",
    )

    return root


def _load_app_from_file(file_path: str) -> Astris:
    target = Path(file_path).expanduser()
    if not target.is_absolute():
        target = Path.cwd() / target
    target = target.resolve()

    if not target.exists():
        raise CliError(f"Python file not found: {target}")
    if not target.is_file():
        raise CliError(f"Path is not a file: {target}")

    module_name = f"astris_build_target_{target.stem}"
    spec = importlib.util.spec_from_file_location(module_name, target)
    if spec is None or spec.loader is None:
        raise CliError(f"Could not load module from: {target}")

    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as error:  # pragma: no cover - exercised via CLI behavior
        raise CliError(f"Failed to execute {target}: {error}") from error

    app = getattr(module, "app", None)
    if app is None:
        raise CliError(f"No 'app' variable found in {target}")
    if not isinstance(app, Astris):
        raise CliError(f"'app' in {target} must be an Astris instance")

    return app


def _load_project_config(base_path: Path | None = None) -> dict[str, Any]:
    root = base_path or Path.cwd()
    pyproject_path = root / "pyproject.toml"
    if not pyproject_path.exists():
        return {}

    try:
        parsed = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as error:
        raise CliError(f"Invalid TOML in {pyproject_path}: {error}") from error

    tool_section = parsed.get("tool", {})
    if not isinstance(tool_section, dict):
        raise CliError("Invalid pyproject.toml: [tool] must be a table")

    astris_section = tool_section.get("astris", {})
    if not isinstance(astris_section, dict):
        raise CliError("Invalid pyproject.toml: [tool.astris] must be a table")

    return astris_section


def _apply_config_env(config: dict[str, Any]) -> None:
    env_section = config.get("env", {})
    if not isinstance(env_section, dict):
        raise CliError("Invalid pyproject.toml: [tool.astris.env] must be a table")

    for key, value in env_section.items():
        os.environ[str(key)] = str(value)


def _extract_build_options(config: dict[str, Any]) -> tuple[str, bool]:
    build_section = config.get("build", {})
    if not isinstance(build_section, dict):
        raise CliError("Invalid pyproject.toml: [tool.astris.build] must be a table")

    output_dir = build_section.get("output_dir", "dist")
    if not isinstance(output_dir, str) or not output_dir.strip():
        raise CliError("Invalid pyproject.toml: build.output_dir must be a string")

    clean_urls = build_section.get("clean_urls", False)
    if not isinstance(clean_urls, bool):
        raise CliError("Invalid pyproject.toml: build.clean_urls must be true/false")

    return output_dir, clean_urls


def _extract_cloudflare_deploy_options(
    config: dict[str, Any],
) -> tuple[str, str | None]:
    deploy_section = config.get("deploy", {})
    if not isinstance(deploy_section, dict):
        raise CliError("Invalid pyproject.toml: [tool.astris.deploy] must be a table")

    provider = deploy_section.get("provider", "cloudflare")
    if provider != "cloudflare":
        raise CliError(
            f"Unsupported deploy provider: {provider}. Supported providers: cloudflare"
        )

    cloudflare_section = deploy_section.get("cloudflare", {})
    if not isinstance(cloudflare_section, dict):
        raise CliError(
            "Invalid pyproject.toml: [tool.astris.deploy.cloudflare] must be a table"
        )

    project_name = cloudflare_section.get("project_name")
    if not isinstance(project_name, str) or not project_name.strip():
        raise CliError(
            "Missing Cloudflare project name. Set tool.astris.deploy.cloudflare.project_name in pyproject.toml"
        )

    branch = cloudflare_section.get("branch")
    if branch is not None and (not isinstance(branch, str) or not branch.strip()):
        raise CliError(
            "Invalid pyproject.toml: deploy.cloudflare.branch must be a non-empty string"
        )

    return project_name, branch


def _run_cloudflare_pages_deploy(
    output_dir: str,
    project_name: str,
    branch: str | None = None,
) -> None:
    command = [
        "npx",
        "wrangler",
        "pages",
        "deploy",
        output_dir,
        "--project-name",
        project_name,
    ]
    if branch:
        command.extend(["--branch", branch])

    try:
        subprocess.run(command, check=True)
    except FileNotFoundError as error:
        raise CliError(
            "Could not run 'npx'. Install Node.js and ensure npx is available."
        ) from error
    except subprocess.CalledProcessError as error:
        raise CliError(
            f"Cloudflare deploy failed with exit code {error.returncode}"
        ) from error


def build_parser() -> argparse.ArgumentParser:
    """Build the top-level Astris CLI parser."""
    parser = argparse.ArgumentParser(
        prog="astris",
        description="Astris CLI",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    new_parser = subparsers.add_parser("new", help="Create a new Astris project")
    new_parser.add_argument("project_name", help="Name of the project directory")

    build_parser = subparsers.add_parser("build", help="Build static site")
    build_parser.add_argument(
        "--file",
        default="main.py",
        help="Python app file to load (default: main.py)",
    )

    deploy_parser = subparsers.add_parser("deploy", help="Build and deploy static site")
    deploy_parser.add_argument(
        "--file",
        default="main.py",
        help="Python app file to load (default: main.py)",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "new":
        try:
            created = create_project(args.project_name)
        except CliError as error:
            print(f"Error: {error}", file=sys.stderr)
            return 2

        print(f"Created Astris project at {created}")
        print("Next steps:")
        print(f"  cd {args.project_name}")
        print("  uv run python main.py")
        return 0

    if args.command == "build":
        try:
            config = _load_project_config()
            _apply_config_env(config)
            output_dir, clean_urls = _extract_build_options(config)
            app = _load_app_from_file(args.file)
            app.build(output_dir=output_dir, clean_urls=clean_urls)
        except CliError as error:
            print(f"Error: {error}", file=sys.stderr)
            return 2

        print(f"Build complete: {output_dir}/")
        return 0

    if args.command == "deploy":
        try:
            config = _load_project_config()
            _apply_config_env(config)
            output_dir, clean_urls = _extract_build_options(config)
            project_name, branch = _extract_cloudflare_deploy_options(config)

            app = _load_app_from_file(args.file)
            app.build(output_dir=output_dir, clean_urls=clean_urls)
            _run_cloudflare_pages_deploy(
                output_dir=output_dir,
                project_name=project_name,
                branch=branch,
            )
        except CliError as error:
            print(f"Error: {error}", file=sys.stderr)
            return 2

        print(f"Deploy complete: cloudflare pages project '{project_name}'")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
