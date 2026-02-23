import types

import astris
from astris import Astris, Text
from astris.lib import Div


def test_page_decorator_registers_route() -> None:
    app = Astris()

    @app.page("/")
    def home():
        return Div(children=[Text("home")])

    assert "/" in app.routes
    assert app.routes["/"].render() == "<div>home</div>"


def test_route_helpers() -> None:
    app = Astris()
    app.routes = {"/": Div(), "/about": Div(), "/blog/": Div()}

    assert app._route_to_filename("/") == "index.html"
    assert app._route_to_filename("/about") == "about.html"
    assert app._route_to_filename("docs/setup") == "docs/setup.html"
    assert app._route_to_filename("/about", clean_urls=True) == "about/index.html"
    assert (
        app._route_to_filename("docs/setup", clean_urls=True)
        == "docs/setup/index.html"
    )

    assert app._resolve_route("/about") == "/about"
    assert app._resolve_route("/blog") == "/blog/"
    assert app._resolve_route("/missing") is None


def test_infer_import_string_from_main_module(monkeypatch) -> None:
    app = Astris()
    fake_main = types.SimpleNamespace(__file__="/tmp/example.py")
    monkeypatch.setitem(__import__("sys").modules, "__main__", fake_main)

    assert app._infer_import_string() == "example:app._fastapi_app"


def test_render_page_html_injects_registered_head_assets() -> None:
    app = Astris()
    app.add_head_link("https://cdn.example.com/bootstrap.css")
    app.add_head_script("https://cdn.example.com/app.js", defer="defer")

    html = app._render_page_html(
        Div(
            children=[
                Text("<html><head><title>Home</title></head><body>Hello</body></html>")
            ]
        )
    )

    assert (
        '<link rel="stylesheet" href="https://cdn.example.com/bootstrap.css">' in html
    )
    assert (
        '<script src="https://cdn.example.com/app.js" defer="defer"></script>' in html
    )
    assert html.index("bootstrap.css") < html.index("</head>")


def test_render_page_html_creates_head_when_missing() -> None:
    app = Astris()
    app.add_head_link("https://cdn.example.com/tailwind.css")

    html = app._render_page_html(
        Div(children=[Text("<html><body>Hello</body></html>")])
    )

    assert "<head>" in html
    assert "tailwind.css" in html


def test_runtime_version_is_exported() -> None:
    assert isinstance(astris.__version__, str)
    assert astris.__version__.count(".") == 2
    assert "__version__" in astris.__all__
