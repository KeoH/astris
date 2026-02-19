from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from pathlib import Path

from .app import AstrisApp

MAIN_TEMPLATE = """import sys

from astris import AstrisApp
from astris.lib import Body, H1, Html

app = AstrisApp()


@app.page("/")
def home():
    return Html(children=[
        Body(children=[
            H1(children=["Hello, world from Astris!"]),
        ])
    ])


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        app.build()
    else:
        app.run_dev()
"""

README_TEMPLATE = """# {project_name}

Project generated with `astris new`.

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

REQUIREMENTS_TEMPLATE = "astris\n"


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
    (root / "requirements.txt").write_text(REQUIREMENTS_TEMPLATE, encoding="utf-8")

    return root


def _load_app_from_file(file_path: str) -> AstrisApp:
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
    if not isinstance(app, AstrisApp):
        raise CliError(f"'app' in {target} must be an AstrisApp instance")

    return app


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
            app = _load_app_from_file(args.file)
            app.build()
        except CliError as error:
            print(f"Error: {error}", file=sys.stderr)
            return 2

        print("Build complete: dist/")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
