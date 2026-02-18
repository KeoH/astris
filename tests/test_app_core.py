import types

from astris import AstrisApp, Text
from astris.lib import Div


def test_page_decorator_registers_route() -> None:
    app = AstrisApp()

    @app.page("/")
    def home():
        return Div(children=[Text("home")])

    assert "/" in app.routes
    assert app.routes["/"].render() == "<div>home</div>"


def test_route_helpers() -> None:
    app = AstrisApp()
    app.routes = {"/": Div(), "/about": Div(), "/blog/": Div()}

    assert app._route_to_filename("/") == "index.html"
    assert app._route_to_filename("/about") == "about.html"
    assert app._route_to_filename("docs/setup") == "docs/setup.html"

    assert app._resolve_route("/about") == "/about"
    assert app._resolve_route("/blog") == "/blog/"
    assert app._resolve_route("/missing") is None


def test_infer_import_string_from_main_module(monkeypatch) -> None:
    app = AstrisApp()
    fake_main = types.SimpleNamespace(__file__="/tmp/example.py")
    monkeypatch.setitem(__import__("sys").modules, "__main__", fake_main)

    assert app._infer_import_string() == "example:app._fastapi_app"
