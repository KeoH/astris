import sys
from typing import Optional

from astris import (
    Astris,
    Text,
    create_default_theme,
    create_soft_theme,
    register_json_collection,
    StyleSheet
)
from astris.components import (
    A,
    Body,
    Button,
    Div,
    H1,
    H2,
    Head,
    Html,
    Li,
    P,
    Section,
    Span,
    Title,
    Ul,
)
from astris.content import JsonCollection
from astris.styles import Align, Display, EdgeInsets, FlexDirection, Style, style

# Use "default" or "soft" to switch the app-level theme preset.
THEME_PRESET = "soft"

base_theme = (
    create_soft_theme("dark")
    if THEME_PRESET == "soft"
    else create_default_theme("dark")
)

# Theme controls app-wide tokens and default component attributes.
theme = base_theme.extend(
    components={
        "body": {
            "style": "margin: 0; background: var(--color-bg); color: var(--color-fg);"
        },
        "Section": {"style": "margin-bottom: var(--space-lg);"},
    },
    extras={
        "global_css": [
            "* { box-sizing: border-box; }",
            "a { color: inherit; }",
        ]
    },
)

app = Astris(theme=theme)

# StyleSheet is a good fit for reusable class-based UI primitives.
stylesheet = StyleSheet()
theme.set_stylesheet(stylesheet)

cls_shell = stylesheet.add_class(
    "shell",
    Style(
        max_width="960px",
        margin="0 auto",
        padding=EdgeInsets.symmetric(vertical=32, horizontal=20),
    ),
    responsive={"md": style(padding=EdgeInsets.symmetric(vertical=24, horizontal=14))},
)

cls_hero = stylesheet.add_class(
    "hero",
    Style(
        display=Display.FLEX,
        flex_direction=FlexDirection.COLUMN,
        gap="14px",
        padding=EdgeInsets.symmetric(vertical=28, horizontal=24),
        border_radius="16px",
        background_color="var(--color-surface)",
        border="1px solid var(--color-surface-contrast)",
        selectors={"& h1": Style(margin=0)},
    ),
    responsive={"md": style(padding=EdgeInsets.symmetric(vertical=20, horizontal=16))},
)

cls_feature_grid = stylesheet.add_class(
    "feature-grid",
    Style(
        display=Display.GRID,
        gap="12px",
        grid_template_columns="repeat(auto-fit, minmax(220px, 1fr))",
    ),
    responsive={"md": style(grid_template_columns="1fr")},
)

cls_card = stylesheet.add_class(
    "card",
    Style(
        padding=EdgeInsets.all(18),
        border_radius="12px",
        background_color="var(--color-surface)",
        border="1px solid var(--color-surface-contrast)",
        selectors={"& h2": Style(margin_top=0, margin_bottom="8px")},
    ),
)

cls_btn = stylesheet.add_class(
    "btn",
    Style(
        display=Display.INLINE_BLOCK,
        text_decoration="none",
        border="none",
        border_radius="10px",
        padding=EdgeInsets.symmetric(vertical=10, horizontal=16),
        cursor="pointer",
        font_weight="600",
        background_color="var(--color-primary)",
        color="var(--color-primary-contrast)",
        states={
            "hover": Style(filter="brightness(1.08)", transform="translateY(-1px)")
        },
    ),
)

cls_btn_subtle = stylesheet.add_class(
    "btn-subtle",
    Style(
        background_color="var(--color-surface-contrast)",
        color="var(--color-fg)",
    ),
)


def main_layout(page_title: str, children: Optional[list] = None) -> Html:
    """Single layout used by all routes to keep theming consistent."""
    return Html(
        children=[
            Head(children=[Title(children=[page_title])]),
            Body(
                children=[
                    Div(class_name=cls_shell, children=children),
                    Div(
                        class_name=cls_shell,
                        style=Style(
                            border_top="1px solid var(--color-surface-contrast)",
                            display=Display.FLEX,
                            justify_content=Align.SPACE_BETWEEN,
                            align_items=Align.CENTER,
                            color="var(--color-muted)",
                        ),
                        children=[
                            Text("Astris demo"),
                            Span(children=[f"Theme preset: {THEME_PRESET}"]),
                        ],
                    ),
                ]
            ),
        ]
    )


def post_template(entry: dict) -> Html:
    """Template used by register_json_collection for each post page."""
    return main_layout(
        page_title=entry.get("title", "Post"),
        children=[
            Div(
                children=[
                    A(
                        href="/posts",
                        class_name=f"{cls_btn} {cls_btn_subtle}",
                        children=["Back to posts"],
                    ),
                ]
            ),
            Section(
                class_name=cls_card,
                children=[
                    H2(children=[entry.get("title", "Untitled")]),
                    P(children=[entry.get("summary", "")]),
                    P(
                        style=Style(color="var(--color-muted)"),
                        children=[
                            f"By {entry.get('author', 'Unknown')} | {entry.get('published_at', 'Unknown date')}"
                        ],
                    ),
                    P(children=[entry.get("content", "")]),
                ],
            ),
        ],
    )


posts_collection: JsonCollection = register_json_collection(
    app,
    name="posts",
    directory="content/posts",
    template=post_template,
    api_prefix="/api/collections",
)


@app.page("/")
def home() -> Html:
    return main_layout(
        page_title="Astris Theme Guide",
        children=[
            Section(
                class_name=cls_hero,
                children=[
                    H1(children=["Astris themes in one file"]),
                    P(
                        children=[
                            "This demo shows a practical relationship between theme tokens, reusable classes, and component composition."
                        ]
                    ),
                    Div(
                        style=Style(display=Display.FLEX, gap="10px"),
                        children=[
                            A(
                                href="/posts",
                                class_name=cls_btn,
                                children=["Browse posts"],
                            ),
                            Button(
                                class_name=f"{cls_btn} {cls_btn_subtle}",
                                children=["Secondary action"],
                            ),
                        ],
                    ),
                ],
            ),
            Section(
                children=[
                    H2(children=["How the pieces fit together"]),
                    Div(
                        class_name=cls_feature_grid,
                        children=[
                            Div(
                                class_name=cls_card,
                                children=[
                                    H2(children=["1) Theme"]),
                                    P(
                                        children=[
                                            "Theme controls colors, spacing, scales, and default attributes for components."
                                        ]
                                    ),
                                ],
                            ),
                            Div(
                                class_name=cls_card,
                                children=[
                                    H2(children=["2) Classes"]),
                                    P(
                                        children=[
                                            "StyleSheet provides reusable classes for shared UI building blocks."
                                        ]
                                    ),
                                ],
                            ),
                            Div(
                                class_name=cls_card,
                                children=[
                                    H2(children=["3) Components"]),
                                    P(
                                        children=[
                                            "Routes compose components with class names and only use inline style for one-off adjustments."
                                        ]
                                    ),
                                ],
                            ),
                        ],
                    ),
                ]
            ),
        ],
    )


@app.page("/posts")
def posts_index() -> Html:
    return main_layout(
        page_title="Posts",
        children=[
            H2(children=["Posts"]),
            P(children=["Generated from JSON files in content/posts."]),
            Ul(
                style=Style(
                    list_style="none",
                    padding=EdgeInsets.all(0),
                    display=Display.FLEX,
                    flex_direction=FlexDirection.COLUMN,
                    gap="10px",
                ),
                children=[
                    Li(
                        children=[
                            A(
                                href=route,
                                class_name=f"{cls_btn} {cls_btn_subtle}",
                                children=[route],
                            )
                        ]
                    )
                    for route in posts_collection.page_links()
                ],
            ),
        ],
    )


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        app.build()
    else:
        app.run_dev()
