from pathlib import Path

from astris import __version__, cli


def test_create_project_generates_expected_files(tmp_path: Path) -> None:
    project_path = cli.create_project("demo_site", base_path=tmp_path)

    assert project_path == tmp_path / "demo_site"
    assert (project_path / "main.py").exists()
    assert (project_path / "README.md").exists()
    assert (project_path / ".gitignore").exists()
    assert not (project_path / "requirements.txt").exists()
    assert (project_path / "pyproject.toml").exists()

    main_content = (project_path / "main.py").read_text(encoding="utf-8")
    pyproject_content = (project_path / "pyproject.toml").read_text(encoding="utf-8")
    assert "app = Astris()" in main_content
    assert '@app.page("/")' in main_content
    assert f'"astris=={__version__}"' in pyproject_content


def test_create_project_fails_if_target_exists(tmp_path: Path) -> None:
    existing = tmp_path / "demo_site"
    existing.mkdir()

    try:
        cli.create_project("demo_site", base_path=tmp_path)
        assert False, "Expected CliError"
    except cli.CliError as error:
        assert "already exists" in str(error)


def test_create_project_rejects_invalid_name(tmp_path: Path) -> None:
    try:
        cli.create_project("123-invalid", base_path=tmp_path)
        assert False, "Expected CliError"
    except cli.CliError as error:
        assert "Invalid project name" in str(error)


def test_main_new_command_returns_success(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    exit_code = cli.main(["new", "hello_app"])

    assert exit_code == 0
    assert (tmp_path / "hello_app" / "main.py").exists()


def test_main_build_command_uses_main_py_by_default(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "main.py").write_text(
        """
from astris import Astris
from astris.lib import Body, Html

app = Astris()


@app.page("/")
def home():
    return Html(children=[Body(children=["hello"])])
""".strip(),
        encoding="utf-8",
    )

    exit_code = cli.main(["build"])

    assert exit_code == 0
    assert (tmp_path / "dist" / "index.html").exists()


def test_main_build_command_supports_custom_file(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "example.py").write_text(
        """
from astris import Astris
from astris.lib import Body, Html

app = Astris()


@app.page("/")
def home():
    return Html(children=[Body(children=["hello from example"])])
""".strip(),
        encoding="utf-8",
    )

    exit_code = cli.main(["build", "--file", "example.py"])

    assert exit_code == 0
    output = (tmp_path / "dist" / "index.html").read_text(encoding="utf-8")
    assert "hello from example" in output


def test_main_build_command_uses_pyproject_build_settings(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "main.py").write_text(
        """
from astris import Astris
from astris.lib import A, Body, Html

app = Astris()


@app.page("/")
def home():
    return Html(children=[Body(children=[A(href="/about", children=["About"])])])


@app.page("/about")
def about():
    return Html(children=[Body(children=["about page"])])
""".strip(),
        encoding="utf-8",
    )
    (tmp_path / "pyproject.toml").write_text(
        """
[tool.astris.build]
output_dir = "public"
clean_urls = true
""".strip(),
        encoding="utf-8",
    )

    exit_code = cli.main(["build"])

    assert exit_code == 0
    assert (tmp_path / "public" / "index.html").exists()
    assert (tmp_path / "public" / "about" / "index.html").exists()


def test_main_build_command_applies_env_from_pyproject(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "main.py").write_text(
        """
import os

from astris import Astris
from astris.lib import Body, Html

app = Astris()


@app.page("/")
def home():
    return Html(children=[Body(children=[os.environ.get("ASTRIS_TEST_ENV", "missing")])])
""".strip(),
        encoding="utf-8",
    )
    (tmp_path / "pyproject.toml").write_text(
        """
[tool.astris.env]
ASTRIS_TEST_ENV = "available"
""".strip(),
        encoding="utf-8",
    )

    exit_code = cli.main(["build"])

    assert exit_code == 0
    output = (tmp_path / "dist" / "index.html").read_text(encoding="utf-8")
    assert "available" in output


def test_main_deploy_runs_cloudflare_pages_command(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "main.py").write_text(
        """
from astris import Astris
from astris.lib import Body, Html

app = Astris()


@app.page("/")
def home():
    return Html(children=[Body(children=["hello"])])
""".strip(),
        encoding="utf-8",
    )
    (tmp_path / "pyproject.toml").write_text(
        """
[tool.astris.build]
output_dir = "dist"
clean_urls = true

[tool.astris.deploy]
provider = "cloudflare"

[tool.astris.deploy.cloudflare]
project_name = "my-pages-project"
branch = "main"
""".strip(),
        encoding="utf-8",
    )

    captured: list[list[str]] = []

    def fake_run(command: list[str], check: bool) -> None:
        assert check is True
        captured.append(command)

    monkeypatch.setattr(cli.subprocess, "run", fake_run)

    exit_code = cli.main(["deploy"])

    assert exit_code == 0
    assert (tmp_path / "dist" / "index.html").exists()
    assert captured == [
        [
            "npx",
            "wrangler",
            "pages",
            "deploy",
            "dist",
            "--project-name",
            "my-pages-project",
            "--branch",
            "main",
        ]
    ]


def test_main_build_command_fails_if_file_missing(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    exit_code = cli.main(["build"])

    assert exit_code == 2


def test_main_build_command_fails_if_app_not_found(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "main.py").write_text("x = 1", encoding="utf-8")

    exit_code = cli.main(["build"])

    assert exit_code == 2


def test_main_build_command_fails_if_app_type_is_invalid(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "main.py").write_text("app = object()", encoding="utf-8")

    exit_code = cli.main(["build"])

    assert exit_code == 2
