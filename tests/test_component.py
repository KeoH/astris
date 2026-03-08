from astris.component import Element, Text
from astris.styles import Align, Display, Style
from astris.theme import Theme, activate_theme, deactivate_theme


class Div(Element):
    tag = "div"


def test_text_render_and_str() -> None:
    text = Text("hola")

    assert text.render() == "hola"
    assert str(text) == "hola"


def test_element_transforms_html_attributes() -> None:
    element = Div(class_name="hero", data_test_id="banner")

    assert element.attributes["class"] == "hero"
    assert element.attributes["data-test-id"] == "banner"


def test_element_renders_children_components_and_strings() -> None:
    element = Div(children=[Text("A"), "B", Div(children=["C"])])

    assert element.render() == "<div>A B<div>C</div></div>".replace(" ", "")


def test_element_style_attribute_accepts_style_instance() -> None:
    element = Div(style=Style(display=Display.FLEX))

    assert "display: flex;" in element.attributes["style"]


def test_element_styles_attribute_merges_style_instances() -> None:
    element = Div(
        styles=[
            Style(display=Display.FLEX, gap="12px"),
            Style(gap="8px", align_items=Align.CENTER),
        ]
    )

    style = element.attributes["style"]
    assert "display: flex;" in style
    assert "gap: 8px;" in style
    assert "align-items: center;" in style


def test_element_style_and_styles_are_merged_together() -> None:
    element = Div(
        style=Style(display=Display.FLEX, gap="12px"),
        styles=[Style(gap="8px", align_items=Align.CENTER)],
    )

    style = element.attributes["style"]
    assert "display: flex;" in style
    assert "gap: 8px;" in style
    assert "align-items: center;" in style


class Img(Element):
    tag = "img"


def test_void_element_renders_without_closing_tag() -> None:
    image = Img(src="/banner.png", alt="banner")

    assert image.render() == '<img src="/banner.png" alt="banner">'


def test_void_element_ignores_children_during_render() -> None:
    image = Img(children=["fallback"], src="/banner.png")

    assert image.render() == '<img src="/banner.png">'


def test_element_applies_theme_defaults_during_render() -> None:
    theme = Theme(
        mode="dark",
        components={
            "div": {"class_name": "surface", "data_variant": "base"},
            "Div": {"data_density": "comfortable"},
        },
    )
    token = activate_theme(theme)

    try:
        element = Div(children=["Hello"])
        rendered = element.render()
    finally:
        deactivate_theme(token)

    assert 'class="surface"' in rendered
    assert 'data-variant="base"' in rendered
    assert 'data-density="comfortable"' in rendered


def test_element_explicit_attributes_override_theme_defaults() -> None:
    theme = Theme(components={"div": {"class_name": "surface", "id": "theme-id"}})
    token = activate_theme(theme)

    try:
        element = Div(class_name="hero", id="custom-id", children=["Hello"])
        rendered = element.render()
    finally:
        deactivate_theme(token)

    assert 'class="hero"' in rendered
    assert 'id="custom-id"' in rendered
    assert 'class="surface"' not in rendered
    assert 'id="theme-id"' not in rendered
