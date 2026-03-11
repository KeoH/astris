import types
from typing import Any

import astris
from astris import Astris, Router, Text
from astris.stylesheet import StyleSheet
from astris.lib import Body, Div, Html
from astris.styles import Style
from astris.theme import Theme


def test_astris_uses_default_theme_when_not_provided() -> None:
    app = Astris()

    assert app.theme is not None
    assert app.theme.extras["name"] == "astris-default"
    assert app.theme.mode == "light"


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
        app._route_to_filename("docs/setup", clean_urls=True) == "docs/setup/index.html"
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
    assert "Theme" in astris.__all__
    assert "StyleSheet" in astris.__all__
    assert "Router" in astris.__all__


def test_render_page_html_injects_theme_style_and_mode_attribute() -> None:
    app = Astris(
        theme=Theme(
            mode="dark",
            colors={"bg": "#111111"},
            spacing={"md": "1rem"},
        )
    )

    html = app._render_page_html(
        Html(children=[Body(children=[Div(children=[Text("home")])])])
    )

    assert 'data-astris-theme="dark"' in html
    assert "--color-bg: #111111;" in html
    assert "--space-md: 1rem;" in html
    assert "color-scheme: dark;" in html
    assert '<html data-theme="dark">' in html


def test_theme_changes_are_reflected_after_page_registration() -> None:
    app = Astris(theme=Theme(mode="light", components={"div": {"class_name": "light"}}))

    @app.page("/")
    def home():
        return Div(children=["home"])

    first_render = app._render_page_html(app.routes["/"])
    app.theme = Theme(mode="dark", components={"div": {"class_name": "dark"}})
    second_render = app._render_page_html(app.routes["/"])

    assert 'class="light"' in first_render
    assert 'class="dark"' in second_render


def test_include_router_registers_prefixed_routes() -> None:
    app = Astris()
    router = Router(prefix="/blog")

    @router.page("/")
    def blog_home():
        return Div(children=[Text("blog")])

    @router.page("/about")
    def blog_about():
        return Div(children=[Text("about")])

    app.include_router(router)

    assert "/blog" in app.routes
    assert "/blog/about" in app.routes


def test_include_router_rejects_non_router_like_objects() -> None:
    app = Astris()

    try:
        app.include_router(object())
    except TypeError as exc:
        assert "iter_pages" in str(exc)
    else:
        raise AssertionError("Expected TypeError for non-router object")


def test_dynamic_route_handles_runtime_params() -> None:
    app = Astris()

    @app.page("/posts/{slug}", static_params=[{"slug": "hello-astris"}])
    def post(slug: str):
        return Div(children=[Text(f"post:{slug}")])

    matching_route: Any = next(
        route for route in app._fastapi_app.routes if getattr(route, "path", None) == "/posts/{slug}"
    )
    response = matching_route.endpoint(slug="hello-astris")

    assert "post:hello-astris" in response


def test_dynamic_route_validates_static_params_keys() -> None:
    app = Astris()

    try:
        @app.page("/posts/{slug}", static_params=[{"bad": "value"}])
        def post(slug: str):
            return Div(children=[Text(slug)])
    except ValueError as exc:
        assert "static_params" in str(exc)
    else:
        raise AssertionError("Expected ValueError for invalid static_params keys")


def test_render_page_html_injects_theme_stylesheets_before_theme_style_and_app_links() -> (
    None
):
    app = Astris(
        theme=Theme(
            mode="light",
            stylesheets=[
                "https://cdn.example.com/base.css",
                "/assets/site.css",
            ],
        )
    )
    app.add_head_link("https://cdn.example.com/app.css")

    html = app._render_page_html(
        Div(
            children=[
                Text("<html><head><title>Home</title></head><body>Hello</body></html>")
            ]
        )
    )

    assert 'href="https://cdn.example.com/base.css"' in html
    assert 'href="/assets/site.css"' in html
    assert 'href="https://cdn.example.com/app.css"' in html
    assert html.index('href="https://cdn.example.com/base.css"') < html.index(
        'data-astris-theme="light"'
    )
    assert html.index('href="/assets/site.css"') < html.index(
        'data-astris-theme="light"'
    )
    assert html.index('data-astris-theme="light"') < html.index(
        'href="https://cdn.example.com/app.css"'
    )


def test_render_page_html_deduplicates_theme_and_app_links_by_href() -> None:
    app = Astris(theme=Theme(stylesheets=["https://cdn.example.com/base.css"]))
    app.add_head_link("https://cdn.example.com/base.css")
    app.add_head_link("https://cdn.example.com/base.css")

    html = app._render_page_html(
        Div(
            children=[
                Text("<html><head><title>Home</title></head><body>Hello</body></html>")
            ]
        )
    )

    assert html.count('href="https://cdn.example.com/base.css"') == 1


def test_render_page_html_injects_attached_theme_stylesheet() -> None:
    stylesheet = StyleSheet()
    stylesheet.add_class("button", style=Style(background_color="#111111"))
    theme = Theme(mode="light")
    theme.set_stylesheet(stylesheet)
    app = Astris(theme=theme)
    app.add_head_link("https://cdn.example.com/app.css")

    html = app._render_page_html(
        Div(
            children=[
                Text("<html><head><title>Home</title></head><body>Hello</body></html>")
            ]
        )
    )

    assert 'data-astris-theme-classes="light"' in html
    assert ".button" in html
    assert "#111111" in html
    assert html.index('data-astris-theme="light"') < html.index(
        'data-astris-theme-classes="light"'
    )
    assert html.index('data-astris-theme-classes="light"') < html.index(
        'href="https://cdn.example.com/app.css"'
    )
