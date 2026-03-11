import os
from pathlib import Path

from astris import Astris


def test_run_dev_uses_reload_import_string_when_available(monkeypatch) -> None:
    app = Astris()
    calls = []

    monkeypatch.setattr(app, "_infer_import_string", lambda: "example:app._fastapi_app")

    def fake_run(*args, **kwargs):
        calls.append((args, kwargs))

    monkeypatch.setattr("astris.app.uvicorn.run", fake_run)

    app.run_dev(port=9001, reload=True)

    assert len(calls) == 1
    args, kwargs = calls[0]
    assert args[0] == "example:app._fastapi_app"
    assert kwargs["reload"] is True
    assert kwargs["port"] == 9001
    assert kwargs["reload_dirs"] == [os.getcwd()]


def test_run_dev_falls_back_when_import_string_is_missing(monkeypatch) -> None:
    app = Astris()
    calls = []

    monkeypatch.setattr(app, "_infer_import_string", lambda: None)

    def fake_run(*args, **kwargs):
        calls.append((args, kwargs))

    monkeypatch.setattr("astris.app.uvicorn.run", fake_run)

    app.run_dev(port=9002, reload=True)

    assert len(calls) == 1
    args, kwargs = calls[0]
    assert args[0] is app._fastapi_app
    assert kwargs["port"] == 9002
    assert "reload" not in kwargs


def test_run_dev_without_reload_uses_fastapi_app(monkeypatch) -> None:
    app = Astris()
    calls = []

    def fake_run(*args, **kwargs):
        calls.append((args, kwargs))

    monkeypatch.setattr("astris.app.uvicorn.run", fake_run)

    app.run_dev(port=9003, reload=False)

    assert len(calls) == 1
    args, kwargs = calls[0]
    assert args[0] is app._fastapi_app
    assert kwargs["port"] == 9003


def test_run_dev_mounts_assets_directory_when_present(
    monkeypatch, tmp_path: Path
) -> None:
    project_root = tmp_path / "project"
    assets_dir = project_root / "assets"
    assets_dir.mkdir(parents=True)
    (assets_dir / "site.css").write_text("body { color: #111; }", encoding="utf-8")

    monkeypatch.chdir(project_root)
    app = Astris()
    calls = []

    def fake_run(*args, **kwargs):
        calls.append((args, kwargs))

    monkeypatch.setattr("astris.app.uvicorn.run", fake_run)

    app.run_dev(port=9004, reload=False)

    assert len(calls) == 1
    assert any(
        getattr(route, "path", None) == "/assets" for route in app._fastapi_app.routes
    )
