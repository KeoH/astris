from astris.css_generator import GlobalStyleSheet
from astris.styles import Display, EdgeInsets, Style, Theme


def test_global_stylesheet_renders_theme_classes_and_raw_css() -> None:
    theme = Theme(name="default", brand_color="#ff5722", surface="#ffffff")
    stylesheet = GlobalStyleSheet(theme=theme)

    button_class = stylesheet.add_class(
        "btn-action",
        Style(
            background_color=theme.brand_color,
            color=theme.surface,
            padding=EdgeInsets.symmetric(vertical=12, horizontal=24),
            border="none",
        ),
    )
    grid_class = stylesheet.add_class(
        "product-grid",
        Style(display=Display.GRID, gap="24px"),
    )
    stylesheet.add_raw(".btn-action:hover { filter: brightness(0.9); }")

    assert button_class == "btn-action"
    assert grid_class == "product-grid"

    css = stylesheet.render_css()
    assert ":root {" in css
    assert "--brand-color: #ff5722;" in css
    assert ".btn-action {" in css
    assert "background-color: var(--brand-color);" in css
    assert ".product-grid {" in css
    assert "display: grid;" in css
    assert ".btn-action:hover" in css

    full = stylesheet.render()
    assert full.startswith("<style>")
    assert full.endswith("</style>")


def test_global_stylesheet_add_media_query_renders_responsive_rules() -> None:
    stylesheet = GlobalStyleSheet()
    stylesheet.add_media_query(
        "(max-width: 768px)",
        {
            ".product-grid": Style(grid_template_columns="1fr", gap="12px"),
            ".hero": "padding: 24px 16px;",
        },
    )

    css = stylesheet.render_css()
    assert "@media (max-width: 768px)" in css
    assert ".product-grid { grid-template-columns: 1fr; gap: 12px; }" in css
    assert ".hero { padding: 24px 16px; }" in css


def test_global_stylesheet_predefined_breakpoint_api() -> None:
    stylesheet = GlobalStyleSheet()
    stylesheet.add_breakpoint(
        "md",
        {
            ".hero": Style(padding=EdgeInsets.symmetric(vertical=24, horizontal=16)),
        },
    )

    css = stylesheet.render_css()
    assert "@media (max-width: 768px)" in css
    assert ".hero { padding: 24px 16px; }" in css


def test_global_stylesheet_custom_breakpoint_and_unknown_key() -> None:
    stylesheet = GlobalStyleSheet()
    stylesheet.set_breakpoint("tablet", "(max-width: 900px)")
    stylesheet.add_breakpoint("tablet", {".grid": Style(grid_template_columns="1fr")})

    css = stylesheet.render_css()
    assert "@media (max-width: 900px)" in css

    try:
        stylesheet.add_breakpoint("unknown", {".x": "display: none;"})
        assert False, "Expected ValueError for unknown breakpoint"
    except ValueError as exc:
        assert "Unknown breakpoint" in str(exc)
