from typing import Optional

from astris.lib import Body, Head, Html, Meta, Title


def astris_ui_layout(content: Optional[list] = None) -> Html:
    return Html(
        children=[
            Head(
                children=[
                    Meta(charset="UTF-8"),
                    Meta(
                        name="viewport", content="width=device-width, initial-scale=1.0"
                    ),
                    Title("Astris Theme UI"),
                ]
            ),
            Body(
                children=(
                    content
                    if content is not None
                    else [
                        "This is the Astris UI layout. The content of the page will be rendered here."
                    ]
                )
            ),
        ]
    )
