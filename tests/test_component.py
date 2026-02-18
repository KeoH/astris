from astris.component import Element, Text


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
