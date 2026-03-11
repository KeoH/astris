from astris.styles import (
    Align,
    Colors,
    Display,
    EdgeInsets,
    FlexDirection,
    PREDEFINED_BREAKPOINTS,
    Position,
    Style,
    TextDecoration,
    TextDecorationLine,
    TextDecorationStyle,
    TextDecorationThickness,
    Theme,
    style,
)


def test_style_renders_typed_values_and_custom_properties() -> None:
    style = Style(
        display=Display.FLEX,
        flex_direction=FlexDirection.COLUMN,
        justify_content=Align.SPACE_BETWEEN,
        align_items=Align.CENTER,
        position=Position.RELATIVE,
        background_color=Colors.WHITE,
        padding=EdgeInsets.all(24),
        margin=EdgeInsets.symmetric(vertical=16, horizontal="auto"),
        box_shadow="0 10px 15px rgba(0,0,0,0.1)",
    )

    css = style.to_css()

    assert "display: flex;" in css
    assert "flex-direction: column;" in css
    assert "justify-content: space-between;" in css
    assert "align-items: center;" in css
    assert "position: relative;" in css
    assert "background-color: #ffffff;" in css
    assert "padding: 24px;" in css
    assert "margin: 16px auto;" in css
    assert "box-shadow: 0 10px 15px rgba(0,0,0,0.1);" in css


def test_edge_insets_factories_render_expected_values() -> None:
    assert str(EdgeInsets.all(10)) == "10px"
    assert str(EdgeInsets.symmetric(vertical=20, horizontal=15)) == "20px 15px"
    assert str(EdgeInsets.only(top=10, bottom=5, left=20)) == "10px 0px 5px 20px"


def test_text_decoration_factories_render_expected_values() -> None:
    assert str(TextDecoration.none()) == "none"
    assert (
        str(
            TextDecoration.underline(
                style=TextDecorationStyle.WAVY,
                color=Colors.BLACK,
                thickness=2,
            )
        )
        == "underline wavy #000000 2px"
    )
    assert (
        str(
            TextDecoration.custom(
                line=[TextDecorationLine.UNDERLINE, TextDecorationLine.OVERLINE],
                style="dashed",
                color="rebeccapurple",
                thickness=TextDecorationThickness.FROM_FONT,
            )
        )
        == "underline overline dashed rebeccapurple from-font"
    )


def test_style_accepts_text_decoration_typed_value() -> None:
    style = Style(
        text_decoration=TextDecoration.line_through(
            style=TextDecorationStyle.DOUBLE,
            color="crimson",
            thickness="0.2em",
        )
    )

    css = style.to_css()
    assert "text-decoration: line-through double crimson 0.2em;" in css


def test_styles_theme_exposes_var_references_and_css_block() -> None:
    theme = Theme(name="core", brand_primary="#3B82F6", spacing_md="16px")

    assert theme.brand_primary == "var(--brand-primary)"
    assert theme.spacing_md == "var(--spacing-md)"

    css = theme.to_style_block()
    assert "--brand-primary: #3B82F6;" in css
    assert "--spacing-md: 16px;" in css


def test_style_merge_and_sx_helpers() -> None:
    base = Style(display=Display.FLEX, gap="12px")
    responsive = style(gap="8px", align_items=Align.CENTER)
    merged = Style.merge(base, responsive, justify_content=Align.SPACE_BETWEEN)

    css = merged.to_css()
    assert "display: flex;" in css
    assert "gap: 8px;" in css
    assert "align-items: center;" in css
    assert "justify-content: space-between;" in css


def test_theme_quick_builder_and_predefined_breakpoints() -> None:
    theme = Theme.quick(name="demo", brand_primary="#7c3aed")

    assert theme.brand_primary == "var(--brand-primary)"
    assert theme.radius_md == "var(--radius-md)"
    assert PREDEFINED_BREAKPOINTS["sm"] == "(max-width: 640px)"
    assert PREDEFINED_BREAKPOINTS["md"] == "(max-width: 768px)"


def test_theme_serializes_enum_tokens_to_css_values() -> None:
    theme = Theme(name="enum-tokens", surface=Colors.BLACK, text_primary=Colors.PINK)

    css = theme.to_style_block()
    assert "--surface: #000000;" in css
    assert "--text-primary: pink;" in css


def test_style_supports_states_and_selectors() -> None:
    style_obj = Style(
        background_color=Colors.WHITE,
        states={
            "hover": Style(color=Colors.BLACK),
            ":focus-visible": "outline: 2px solid var(--color-primary);",
        },
        selectors={
            ":nth-child(odd)": Style(background_color=Colors.GHOST_WHITE),
            "& > h2": Style(margin_bottom="8px"),
        },
    )

    rules = style_obj.nested_rules_for(".card")
    rules_map = {selector: declarations for selector, declarations in rules}

    assert rules_map[".card:hover"] == "color: #000000;"
    assert (
        rules_map[".card:focus-visible"] == "outline: 2px solid var(--color-primary);"
    )
    assert rules_map[".card:nth-child(odd)"] == "background-color: ghostwhite;"
    assert rules_map[".card > h2"] == "margin-bottom: 8px;"


def test_style_merge_preserves_nested_rules() -> None:
    base = Style(states={"hover": Style(color=Colors.BLACK)})
    override = Style(selectors={"& > .icon": Style(margin_left="6px")})

    merged = Style.merge(base, override, display=Display.INLINE_BLOCK)
    merged_css = merged.to_css()
    merged_rules = {s: d for s, d in merged.nested_rules_for(".btn")}

    assert "display: inline-block;" in merged_css
    assert merged_rules[".btn:hover"] == "color: #000000;"
    assert merged_rules[".btn > .icon"] == "margin-left: 6px;"
