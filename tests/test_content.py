import json
from pathlib import Path
from typing import Callable

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from astris import AstrisApp, Text
from astris.content import register_json_collection
from astris.lib import Div


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


def _route_endpoint(app: AstrisApp, path: str) -> Callable[..., JSONResponse]:
    for route in app._fastapi_app.routes:
        if getattr(route, "path", None) == path:
            endpoint = getattr(route, "endpoint", None)
            if callable(endpoint):
                return endpoint
            break
    raise AssertionError(f"Route not found: {path}")


def test_register_json_collection_generates_detail_routes_and_build(
    tmp_path: Path,
) -> None:
    app = AstrisApp()
    posts_dir = tmp_path / "posts"
    posts_dir.mkdir()

    _write_json(posts_dir / "hello-world.json", {"title": "Hello"})
    _write_json(posts_dir / "custom.json", {"slug": "custom-slug", "title": "Custom"})

    collection = register_json_collection(
        app,
        name="posts",
        directory=posts_dir,
        template=lambda entry: Div(children=[Text(entry["title"])]),
    )

    assert collection.page_links() == ["/posts/custom-slug", "/posts/hello-world"]

    output_dir = tmp_path / "site"
    app.build(str(output_dir))

    assert (output_dir / "posts/custom-slug.html").exists()
    assert (output_dir / "posts/hello-world.html").exists()


def test_register_json_collection_exposes_read_only_api(tmp_path: Path) -> None:
    app = AstrisApp()
    posts_dir = tmp_path / "posts"
    posts_dir.mkdir()

    _write_json(posts_dir / "first.json", {"slug": "first", "title": "First"})

    register_json_collection(
        app,
        name="posts",
        directory=posts_dir,
        template=lambda entry: Div(children=[Text(entry["title"])]),
        api_prefix="/content-api",
    )

    list_endpoint = _route_endpoint(app, "/content-api/posts")
    detail_endpoint = _route_endpoint(app, "/content-api/posts/{slug}")

    list_response = list_endpoint()
    assert isinstance(list_response, JSONResponse)
    list_payload = json.loads(bytes(list_response.body).decode("utf-8"))
    assert len(list_payload) == 1
    assert list_payload[0]["slug"] == "first"
    assert list_payload[0]["route"] == "/posts/first"

    detail_response = detail_endpoint(slug="first")
    assert isinstance(detail_response, JSONResponse)
    detail_payload = json.loads(bytes(detail_response.body).decode("utf-8"))
    assert detail_payload["data"]["title"] == "First"

    try:
        detail_endpoint(slug="missing")
    except HTTPException as exc:
        assert exc.status_code == 404
    else:
        raise AssertionError("Expected HTTPException(404) for missing collection slug")


def test_register_json_collection_template_must_return_component(
    tmp_path: Path,
) -> None:
    app = AstrisApp()
    posts_dir = tmp_path / "posts"
    posts_dir.mkdir()
    _write_json(posts_dir / "first.json", {"title": "First"})

    try:
        register_json_collection(
            app,
            name="posts",
            directory=posts_dir,
            template=lambda entry: entry,
        )
    except TypeError as exc:
        assert "Component" in str(exc)
    else:
        raise AssertionError(
            "register_json_collection should fail for invalid template"
        )
