from typing import Optional

from astris.lib import Body, Head, Html, Meta, Title


def bootstrap_layout(page_title: str = "Astris Bootstrap Theme", content: Optional[list] = None) -> Html:
    return Html(
        children=[
            Head(
                children=[
                    Meta(charset="UTF-8"),
                    Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
                    Title(page_title),
                ]
            ),
            Body(
                class_name="theme-shell",
                children=(
                    content
                    if content is not None
                    else [
                        "This is the Bootstrap theme layout. Add your page content here.",
                    ]
                ),
            ),
        ]
    )
