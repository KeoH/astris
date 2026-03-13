# Theme Examples

## Theme package imports

```python
from astris import Astris
from astris.themes.my_theme import theme

app = Astris(theme=theme)
```

## Reusable component wrapper pattern

```python
from astris.lib import Article, H3, P


class SimpleCard(Article):
    def __init__(self, title: str, content: str, **kwargs):
        super().__init__(
            class_name="card",
            children=[
                H3(title, class_name="card-title"),
                P(content, class_name="card-content"),
            ],
            **kwargs,
        )
```

## Layout helper pattern

```python
from astris.lib import Body, Head, Html, Meta, Title


def app_layout(content: list):
    return Html(
        children=[
            Head(children=[Meta(charset="UTF-8"), Title("My Theme")]),
            Body(children=content),
        ]
    )
```
