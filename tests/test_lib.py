from astris.lib import A, Column, Container, Head, Html, Row, Title


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


def test_column_and_row_include_default_flex_style() -> None:
    column = Column(children=["x"])
    row = Row(children=["y"])

    assert "flex-direction: column" in column.render()
    assert "flex-direction: row" in row.render()
