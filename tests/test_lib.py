import inspect

import astris.lib as lib
from astris.component import Element
from astris.layout import Column, Container, Row
from astris.lib import A, Br, Head, Html, Img, Title


def test_html_wrappers_render_expected_tags() -> None:
    page = Html(
        children=[
            Head(children=[Title(children=["Demo"])]),
            Container(children=[A(href="/", children=["Inicio"])]),
        ]
    )
    html = page.render()

    assert "<html>" in html
    assert "<head>" in html
    assert "<title>Demo</title>" in html
    assert '<a href="/">Inicio</a>' in html


def test_void_wrappers_render_without_closing_tag() -> None:
    image = Img(src="/logo.png", alt="logo")
    line_break = Br()

    assert image.render() == '<img src="/logo.png" alt="logo">'
    assert line_break.render() == "<br>"


def test_column_and_row_include_default_flex_style() -> None:
    column = Column(children=["x"])
    row = Row(children=["y"])

    assert "flex-direction: column" in column.render()
    assert "flex-direction: row" in row.render()


def test_all_element_classes_in_lib_include_docstrings() -> None:
    element_classes = [
        value
        for _, value in vars(lib).items()
        if inspect.isclass(value)
        and issubclass(value, Element)
        and value is not Element
    ]

    assert element_classes
    for cls in element_classes:
        assert cls.__doc__ is not None
        assert cls.__doc__.strip()


def test_lib_includes_expected_core_html_wrappers() -> None:
    expected = {
        "Html",
        "Head",
        "Body",
        "Main",
        "Section",
        "Header",
        "Footer",
        "Nav",
        "Form",
        "Input",
        "Button",
        "Select",
        "Textarea",
        "Table",
        "Video",
        "Audio",
        "Canvas",
        "Template",
    }

    available = {name for name, value in vars(lib).items() if inspect.isclass(value)}
    assert expected.issubset(available)
