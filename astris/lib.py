from .component import Element


class Html(Element):
    tag = "html"


class Head(Element):
    tag = "head"


class Body(Element):
    tag = "body"


class Div(Element):
    tag = "div"


class Span(Element):
    tag = "span"


class H1(Element):
    tag = "h1"


class H2(Element):
    tag = "h2"


class P(Element):
    tag = "p"


class A(Element):
    tag = "a"


class Ul(Element):
    tag = "ul"

class Use(Element):
    """Represents a <use> element in SVG."""

    tag = "use"

class Li(Element):
    tag = "li"


class Button(Element):
    tag = "button"


class Title(Element):
    tag = "title"


class Container(Div):
    pass


class Column(Div):
    def __init__(self, children=None, **kwargs):
        super().__init__(
            children, style="display: flex; flex-direction: column;", **kwargs
        )


class Row(Div):
    def __init__(self, children=None, **kwargs):
        super().__init__(
            children, style="display: flex; flex-direction: row;", **kwargs
        )
