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

from astris import Astris, Theme, StyleSheet
from astris.lib import A, Body, Button, Div, H1, Header, Html, Main, P, Span

theme = Theme(
    name="Starter Theme",
    stylesheets=["https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css"],
)
theme.set_stylesheet(StyleSheet())
app = Astris(theme=theme)


@app.page("/")
def home():
    return Html(
        **{"lang": "en", "class": "scroll-smooth"},
        children=[
            Body(
                **{
                    "class": "bg-slate-950 text-slate-100 min-h-screen flex flex-col font-sans antialiased selection:bg-indigo-500/30 selection:text-indigo-200"
                },
                children=[
                    # Background Effect
                    Div(
                        **{"class": "fixed inset-0 z-[-1]", "aria-hidden": "true"},
                        children=[
                            Div(
                                **{
                                    "class": "absolute top-0 -left-4 w-96 h-96 bg-indigo-500 rounded-full mix-blend-multiply filter blur-[128px] opacity-20 animate-pulse"
                                },
                                children=[]
                            ),
                            Div(
                                **{
                                    "class": "absolute top-0 -right-4 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-[128px] opacity-20 animate-pulse animation-delay-2000"
                                },
                                children=[]
                            ),
                            Div(
                                **{
                                    "class": "absolute -bottom-8 left-20 w-96 h-96 bg-pink-500 rounded-full mix-blend-multiply filter blur-[128px] opacity-20 animate-pulse animation-delay-4000"
                                },
                                children=[]
                            ),
                        ]
                    ),
                    # Header Navigation
                    Header(
                        **{
                            "class": "w-full py-6 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto flex items-center justify-between"
                        },
                        children=[
                            Div(
                                **{
                                    "class": "flex items-center gap-2 group cursor-pointer"
                                },
                                children=[
                                    Div(
                                        **{
                                            "class": "w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center transform group-hover:rotate-12 transition-transform duration-300 shadow-lg shadow-indigo-500/30"
                                        },
                                        children=[
                                            Span(
                                                **{
                                                    "class": "text-white font-bold text-lg"
                                                },
                                                children=["A"]
                                            )
                                        ]
                                    ),
                                    Span(
                                        **{
                                            "class": "text-xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400"
                                        },
                                        children=["Astris"]
                                    ),
                                ]
                            ),
                            Div(
                                **{
                                    "class": "flex items-center gap-6 text-sm font-medium"
                                },
                                children=[
                                    A(
                                        **{
                                            "href": "https://astris.readthedocs.io",
                                            "target": "_blank",
                                            "rel": "noopener noreferrer",
                                            "class": "text-slate-300 hover:text-white transition-colors",
                                        },
                                        children=["Documentation"]
                                    ),
                                    A(
                                        **{
                                            "href": "https://github.com/keoh/astris",
                                            "target": "_blank",
                                            "rel": "noopener noreferrer",
                                            "class": "text-slate-300 hover:text-white transition-colors",
                                        },
                                        children=["GitHub"]
                                    ),
                                ]
                            ),
                        ]
                    ),
                    # Main Content area (Hero Section)
                    Main(
                        **{
                            "class": "flex-grow flex flex-col items-center justify-center px-4 sm:px-6 lg:px-8 text-center mt-12 mb-24"
                        },
                        children=[
                            # Badge
                            A(
                                **{
                                    "href": "https://astris.readthedocs.io",
                                    "target": "_blank",
                                    "class": "inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-800/50 border border-slate-700/50 text-sm font-medium text-slate-300 mb-8 backdrop-blur-sm hover:bg-slate-800 hover:border-slate-600 transition-all cursor-pointer group",
                                },
                                children=[
                                    Span(
                                        **{"class": "relative flex h-2 w-2"},
                                        children=[
                                            Span(
                                                **{
                                                    "class": "animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"
                                                },
                                                children=[]
                                            ),
                                            Span(
                                                **{
                                                    "class": "relative inline-flex rounded-full h-2 w-2 bg-indigo-500"
                                                },
                                                children=[]
                                            ),
                                        ]
                                    ),
                                    Span(children=["Astris Framework Ready"]),
                                    Span(
                                        **{
                                            "class": "text-indigo-400 group-hover:translate-x-1 transition-transform"
                                        },
                                        children=["→"]
                                    ),
                                ]
                            ),
                            # Title
                            H1(
                                **{
                                    "class": "text-5xl sm:text-6xl md:text-7xl font-extrabold tracking-tight mb-8 max-w-4xl mx-auto"
                                },
                                children=[
                                    Span(children=["Build static websites "]),
                                    Span(**{"class": "inline-block"}, children=[]),
                                    Span(
                                        **{
                                            "class": "text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 hover:from-pink-400 hover:to-indigo-400 transition-all duration-1000"
                                        },
                                        children=["elegantly"]
                                    ),
                                ]
                            ),
                            # Description
                            P(
                                **{
                                    "class": "text-lg sm:text-xl text-slate-400 mb-10 max-w-2xl mx-auto leading-relaxed"
                                },
                                children=[
                                    "You are looking at your new Astris application. It's time to start building something amazing using component-style APIs in Python."
                                ]
                            ),
                            # Action Buttons
                            Div(
                                **{
                                    "class": "flex flex-col sm:flex-row gap-4 justify-center"
                                },
                                children=[
                                    A(
                                        **{
                                            "href": "https://astris.readthedocs.io/en/latest/quickstart/",
                                            "target": "_blank",
                                            "rel": "noopener noreferrer",
                                        },
                                        children=[
                                            Button(
                                                **{
                                                    "class": "px-8 py-4 w-full sm:w-auto rounded-xl bg-white text-slate-900 font-bold hover:bg-slate-100 hover:scale-[1.02] shadow-[0_0_40px_-10px_rgba(255,255,255,0.3)] transition-all duration-200 active:scale-95"
                                                },
                                                children=["Get Started"]
                                            )
                                        ]
                                    ),
                                    A(
                                        **{
                                            "href": "https://astris.readthedocs.io/en/latest/api/",
                                            "target": "_blank",
                                            "rel": "noopener noreferrer",
                                        },
                                        children=[
                                            Button(
                                                **{
                                                    "class": "px-8 py-4 w-full sm:w-auto rounded-xl bg-slate-800/80 text-white font-bold border border-slate-700 hover:bg-slate-800 hover:border-slate-500 hover:shadow-lg backdrop-blur-sm transition-all duration-200 active:scale-95"
                                                },
                                                children=["View API Reference"]
                                            )
                                        ]
                                    ),
                                ]
                            ),
                            # Code Snippet Preview (Glassmorphism card)
                            Div(
                                **{
                                    "class": "mt-16 w-full max-w-2xl mx-auto text-left relative group"
                                },
                                children=[
                                    # Decorative gradient border
                                    Div(
                                        **{
                                            "class": "absolute -inset-[1px] bg-gradient-to-r from-indigo-500/50 via-purple-500/50 to-pink-500/50 rounded-2xl blur-sm opacity-50 group-hover:opacity-100 transition duration-500"
                                        },
                                        children=[]
                                    ),
                                    Div(
                                        **{
                                            "class": "relative bg-slate-900/80 backdrop-blur-xl border border-slate-700/50 rounded-2xl overflow-hidden shadow-2xl"
                                        },
                                        children=[
                                            Div(
                                                **{
                                                    "class": "flex items-center px-4 py-3 bg-slate-800/50 border-b border-slate-700/50"
                                                },
                                                children=[
                                                    Div(
                                                        **{"class": "flex gap-2"},
                                                        children=[
                                                            Div(
                                                                **{
                                                                    "class": "w-3 h-3 rounded-full bg-red-500/80"
                                                                },
                                                                children=[]
                                                            ),
                                                            Div(
                                                                **{
                                                                    "class": "w-3 h-3 rounded-full bg-yellow-500/80"
                                                                },
                                                                children=[]
                                                            ),
                                                            Div(
                                                                **{
                                                                    "class": "w-3 h-3 rounded-full bg-green-500/80"
                                                                },
                                                                children=[]
                                                            ),
                                                        ]
                                                    ),
                                                    Span(
                                                        **{
                                                            "class": "ml-4 text-xs font-mono text-slate-400"
                                                        },
                                                        children=["main.py"]
                                                    ),
                                                ]
                                            ),
                                            Div(
                                                **{"class": "p-6 overflow-x-auto"},
                                                children=[
                                                    P(
                                                        **{
                                                            "class": "font-mono text-sm leading-relaxed"
                                                        },
                                                        children=[
                                                            Span(
                                                                **{
                                                                    "class": "text-purple-400"
                                                                },
                                                                children=["from "]
                                                            ),
                                                            Span(
                                                                **{
                                                                    "class": "text-slate-300"
                                                                },
                                                                children=["astris "]
                                                            ),
                                                            Span(
                                                                **{
                                                                    "class": "text-purple-400"
                                                                },
                                                                children=["import "]
                                                            ),
                                                            Span(
                                                                **{
                                                                    "class": "text-yellow-200"
                                                                },
                                                                children=["Astris"]
                                                            ),
                                                            Div(
                                                                **{"class": "h-2"},
                                                                children=[]
                                                            ),
                                                            Span(
                                                                **{
                                                                    "class": "text-slate-300"
                                                                },
                                                                children=["app = "]
                                                            ),
                                                            Span(
                                                                **{
                                                                    "class": "text-yellow-200"
                                                                },
                                                                children=["Astris"]
                                                            ),
                                                            Span(
                                                                **{
                                                                    "class": "text-slate-300"
                                                                },
                                                                children=["()"]
                                                            ),
                                                            Div(
                                                                **{"class": "h-2"},
                                                                children=[]
                                                            ),
                                                            Span(
                                                                **{
                                                                    "class": "text-yellow-400"
                                                                },
                                                                children=["@app.page"]
                                                            ),
                                                            Span(
                                                                **{
                                                                    "class": "text-slate-300"
                                                                },
                                                                children=["("]
                                                            ),
                                                            Span(
                                                                **{
                                                                    "class": "text-green-300"
                                                                },
                                                                children=['"/"']
                                                            ),
                                                            Span(
                                                                **{
                                                                    "class": "text-slate-300"
                                                                },
                                                                children=[")"]
                                                            ),
                                                            Div(
                                                                **{"class": "h-0"},
                                                                children=[]
                                                            ),
                                                            Span(
                                                                **{
                                                                    "class": "text-purple-400"
                                                                },
                                                                children=["def "]
                                                            ),
                                                            Span(
                                                                **{
                                                                    "class": "text-blue-300"
                                                                },
                                                                children=["home"]
                                                            ),
                                                            Span(
                                                                **{
                                                                    "class": "text-slate-300"
                                                                },
                                                                children=["():"]
                                                            ),
                                                            Div(
                                                                **{"class": "h-0"},
                                                                children=[]
                                                            ),
                                                            Span(
                                                                **{
                                                                    "class": "text-slate-300 pl-4"
                                                                },
                                                                children=["..."]
                                                            ),
                                                        ]
                                                    )
                                                ]
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]
            )
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
