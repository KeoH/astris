from astris.layout import Column, Container, Row


def test_layout_wrappers_render_div_tag() -> None:
    container = Container(children=["content"])
    column = Column(children=["content"])
    row = Row(children=["content"])

    assert container.render() == "<div>content</div>"
    assert (
        column.render()
        == '<div style="display: flex; flex-direction: column; gap: var(--space-md, 1rem);">content</div>'
    )
    assert (
        row.render()
        == '<div style="display: flex; flex-direction: row; gap: var(--space-md, 1rem);">content</div>'
    )


def test_layout_kwargs_override_default_style() -> None:
    row = Row(children=["content"], style="display: block;")

    assert row.render() == '<div style="display: block;">content</div>'
