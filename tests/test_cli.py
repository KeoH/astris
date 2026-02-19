from pathlib import Path

from astris import cli


def test_create_project_generates_expected_files(tmp_path: Path) -> None:
    project_path = cli.create_project("demo_site", base_path=tmp_path)

    assert project_path == tmp_path / "demo_site"
    assert (project_path / "main.py").exists()
    assert (project_path / "README.md").exists()
    assert (project_path / ".gitignore").exists()
    assert (project_path / "requirements.txt").exists()

    main_content = (project_path / "main.py").read_text(encoding="utf-8")
    assert "app = AstrisApp()" in main_content
    assert '@app.page("/")' in main_content


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
from astris import AstrisApp
from astris.lib import Body, Html

app = AstrisApp()


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
from astris import AstrisApp
from astris.lib import Body, Html

app = AstrisApp()


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
