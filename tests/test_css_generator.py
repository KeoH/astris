from astris.stylesheet import StyleSheet
from astris.styles import Display, EdgeInsets, Style, Theme


def test_global_stylesheet_renders_theme_classes_and_raw_css() -> None:
    theme = Theme(name="default", brand_color="#ff5722", surface="#ffffff")
    stylesheet = StyleSheet(theme=theme)

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
    stylesheet = StyleSheet()
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
    stylesheet = StyleSheet()
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
    stylesheet = StyleSheet()
    stylesheet.set_breakpoint("tablet", "(max-width: 900px)")
    stylesheet.add_breakpoint("tablet", {".grid": Style(grid_template_columns="1fr")})

    css = stylesheet.render_css()
    assert "@media (max-width: 900px)" in css

    try:
        stylesheet.add_breakpoint("unknown", {".x": "display: none;"})
        assert False, "Expected ValueError for unknown breakpoint"
    except ValueError as exc:
        assert "Unknown breakpoint" in str(exc)


def test_add_class_with_responsive_single_breakpoint() -> None:
    stylesheet = StyleSheet()

    stylesheet.add_class(
        "card",
        Style(padding="16px", display=Display.GRID),
        responsive={"md": Style(padding="12px")},
    )

    css = stylesheet.render_css()
    assert ".card {" in css
    assert "display: grid;" in css
    assert "padding: 16px;" in css
    assert "@media (max-width: 768px) { .card { padding: 12px; } }" in css


def test_add_class_with_responsive_multiple_breakpoints() -> None:
    stylesheet = StyleSheet()

    stylesheet.add_class(
        "grid",
        Style(grid_template_columns="repeat(3, 1fr)", gap="24px"),
        responsive={
            "lg": Style(grid_template_columns="repeat(2, 1fr)"),
            "md": Style(grid_template_columns="1fr", gap="12px"),
        },
    )

    css = stylesheet.render_css()
    assert (
        "@media (max-width: 1024px) { .grid { grid-template-columns: repeat(2, 1fr); } }"
        in css
    )
    assert (
        "@media (max-width: 768px) { .grid { grid-template-columns: 1fr; gap: 12px; } }"
        in css
    )


def test_add_class_with_responsive_supports_raw_css_string() -> None:
    stylesheet = StyleSheet()

    stylesheet.add_class(
        "btn",
        Style(padding="10px"),
        responsive={"sm": "padding: 8px;"},
    )

    css = stylesheet.render_css()
    assert "@media (max-width: 640px) { .btn { padding: 8px; } }" in css


def test_add_class_with_responsive_rejects_unknown_breakpoint() -> None:
    stylesheet = StyleSheet()

    try:
        stylesheet.add_class(
            "card",
            Style(padding="16px"),
            responsive={"phone": Style(padding="8px")},
        )
        assert False, "Expected ValueError for unknown breakpoint"
    except ValueError as exc:
        assert "Unknown breakpoint 'phone'" in str(exc)


def test_add_class_with_empty_responsive_does_not_create_media_rules() -> None:
    stylesheet = StyleSheet()

    stylesheet.add_class("card", Style(padding="16px"), responsive={})

    css = stylesheet.render_css()
    assert ".card { padding: 16px; }" in css
    assert "@media" not in css


def test_add_class_renders_style_states_and_selectors() -> None:
    stylesheet = StyleSheet()

    stylesheet.add_class(
        "btn",
        Style(
            padding="10px",
            states={"hover": Style(filter="brightness(1.08)")},
            selectors={":nth-child(odd)": Style(background_color="#fafafa")},
        ),
    )

    css = stylesheet.render_css()
    assert ".btn { padding: 10px; }" in css
    assert ".btn:hover { filter: brightness(1.08); }" in css
    assert ".btn:nth-child(odd) { background-color: #fafafa; }" in css


def test_add_class_renders_responsive_nested_style_rules() -> None:
    stylesheet = StyleSheet()

    stylesheet.add_class(
        "btn",
        Style(padding="10px"),
        responsive={
            "md": Style(
                padding="8px",
                states={"hover": Style(filter="brightness(1.02)")},
            )
        },
    )

    css = stylesheet.render_css()
    assert "@media (max-width: 768px)" in css
    assert ".btn { padding: 8px; }" in css
    assert ".btn:hover { filter: brightness(1.02); }" in css
