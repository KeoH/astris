from pathlib import Path

from astris import Astris, Text, Theme
from astris.lib import A, Div


def test_build_generates_static_files_and_doctype(tmp_path: Path) -> None:
    app = Astris()

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
    app = Astris()

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
    app = Astris()
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


def test_build_with_clean_urls_generates_index_folders_and_clean_links(
    tmp_path: Path,
) -> None:
    app = Astris()

    @app.page("/")
    def home():
        return Div(children=[A(href="/about", children=["About"])])

    @app.page("/about")
    def about():
        return Div(
            children=[
                A(href="/", children=["Home"]),
                A(href="/about?tab=team#top", children=["Anchor"]),
            ]
        )

    output_dir = tmp_path / "site"
    app.build(str(output_dir), clean_urls=True)

    index_file = output_dir / "index.html"
    about_file = output_dir / "about" / "index.html"

    assert index_file.exists()
    assert about_file.exists()

    index_html = index_file.read_text(encoding="utf-8")
    about_html = about_file.read_text(encoding="utf-8")

    assert 'href="/about"' in index_html
    assert 'href="/"' in about_html
    assert 'href="/about?tab=team#top"' in about_html


def test_build_includes_theme_stylesheets_and_deduplicates_with_app_links(
    tmp_path: Path,
) -> None:
    app = Astris(
        theme=Theme(
            stylesheets=[
                "https://cdn.example.com/base.css",
                "/assets/site.css",
            ]
        )
    )
    app.add_head_link("https://cdn.example.com/base.css")

    @app.page("/docs/intro")
    def docs_intro():
        return Div(
            children=[
                Text(
                    "<html><head><title>Docs</title></head><body><h1>Docs</h1></body></html>"
                )
            ]
        )

    output_dir = tmp_path / "site"
    app.build(str(output_dir))

    docs_html = (output_dir / "docs/intro.html").read_text(encoding="utf-8")

    assert 'href="https://cdn.example.com/base.css"' in docs_html
    assert 'href="/assets/site.css"' in docs_html
    assert docs_html.count('href="https://cdn.example.com/base.css"') == 1


def test_build_rewrites_relative_theme_assets_stylesheets_for_nested_routes(
    tmp_path: Path,
) -> None:
    app = Astris(
        theme=Theme(
            stylesheets=[
                "assets/site.css",
            ]
        )
    )

    @app.page("/")
    def home():
        return Div(children=[Text("<html><body>Home</body></html>")])

    @app.page("/docs/intro")
    def docs_intro():
        return Div(children=[Text("<html><body>Docs</body></html>")])

    output_dir = tmp_path / "site"
    app.build(str(output_dir))

    index_html = (output_dir / "index.html").read_text(encoding="utf-8")
    docs_html = (output_dir / "docs/intro.html").read_text(encoding="utf-8")

    assert 'href="assets/site.css"' in index_html
    assert 'href="../assets/site.css"' in docs_html


def test_build_copies_assets_directory(tmp_path: Path, monkeypatch) -> None:
    app = Astris()

    @app.page("/")
    def home():
        return Div(children=[Text("<html><body>Home</body></html>")])

    project_root = tmp_path / "project"
    assets_dir = project_root / "assets"
    assets_dir.mkdir(parents=True)
    (assets_dir / "site.css").write_text("body { color: #222; }", encoding="utf-8")
    (assets_dir / "scripts").mkdir()
    (assets_dir / "scripts" / "app.js").write_text(
        "console.log('hello');", encoding="utf-8"
    )

    output_dir = project_root / "dist"
    monkeypatch.chdir(project_root)
    app.build(str(output_dir))

    assert (output_dir / "assets" / "site.css").exists()
    assert (output_dir / "assets" / "scripts" / "app.js").exists()
