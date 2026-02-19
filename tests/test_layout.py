from astris.layout import Column, Container, Row


def test_layout_wrappers_render_div_tag() -> None:
    container = Container(children=["content"])
    column = Column(children=["content"])
    row = Row(children=["content"])

    assert container.render() == "<div>content</div>"
    assert (
        column.render()
        == '<div style="display: flex; flex-direction: column;">content</div>'
    )
    assert (
        row.render() == '<div style="display: flex; flex-direction: row;">content</div>'
    )
