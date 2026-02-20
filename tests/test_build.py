from pathlib import Path

from astris import AstrisApp, Text
from astris.lib import A, Div


def test_build_generates_static_files_and_doctype(tmp_path: Path) -> None:
    app = AstrisApp()

    @app.page("/")
    def home():
        return Div(
            children=[
                A(href="/about", children=["About"]),
                Text(" "),
                A(href="https://example.com", children=["Externo"]),
            ]
        )

    @app.page("/about")
    def about():
        return Div(
            children=[
                A(href="/", children=["Inicio"]),
                A(href="/about?tab=team#top", children=["Anchor"]),
            ]
        )

    output_dir = tmp_path / "site"
    app.build(str(output_dir))

    index_file = output_dir / "index.html"
    about_file = output_dir / "about.html"

    assert index_file.exists()
    assert about_file.exists()

    index_html = index_file.read_text(encoding="utf-8")
    about_html = about_file.read_text(encoding="utf-8")

    assert index_html.startswith("<!DOCTYPE html>")
    assert about_html.startswith("<!DOCTYPE html>")
    assert 'href="about.html"' in index_html
    assert 'href="https://example.com"' in index_html
    assert 'href="index.html"' in about_html
    assert 'href="about.html?tab=team#top"' in about_html


def test_build_rewrites_relative_links_for_nested_routes(tmp_path: Path) -> None:
    app = AstrisApp()

    @app.page("/about")
    def about():
        return Div(children=[Text("About")])

    @app.page("/docs/getting-started")
    def docs():
        return Div(
            children=[
                A(href="/about", children=["About"]),
                A(href="/missing", children=["Missing"]),
            ]
        )

    output_dir = tmp_path / "site"
    app.build(str(output_dir))

    docs_html = (output_dir / "docs/getting-started.html").read_text(encoding="utf-8")

    assert 'href="../about.html"' in docs_html
    assert 'href="/missing"' in docs_html


def test_build_includes_registered_head_assets(tmp_path: Path) -> None:
    app = AstrisApp()
    app.add_head_link(
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
    )
    app.add_head_script(
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"
    )

    @app.page("/")
    def home():
        return Div(
            children=[
                Text(
                    "<html><head><title>Home</title></head><body><h1>Hi</h1></body></html>"
                )
            ]
        )

    output_dir = tmp_path / "site"
    app.build(str(output_dir))

    index_html = (output_dir / "index.html").read_text(encoding="utf-8")

    assert "bootstrap.min.css" in index_html
    assert "bootstrap.bundle.min.js" in index_html
