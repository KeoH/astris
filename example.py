import sys
from typing import Optional

# Simulate that astris is an installed package
from astris import Astris, Text, create_default_theme, create_soft_theme, register_json_collection
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
from astris.css_generator import GlobalStyleSheet
from astris.styles import Align, Colors, Display, EdgeInsets, FlexDirection, Style, Theme as CssTheme, style

# 1. Initialize the app
# Change this to "default" to use Astris default tokens.
THEME_PRESET = "soft"

theme = (
    create_soft_theme("dark")
    if THEME_PRESET == "soft"
    else create_default_theme("dark")
)

app = Astris(theme=theme)

css_theme = CssTheme.quick(
    name="demo",
    brand_primary = Colors.INDIGO,
    surface=Colors.GAINSBORO,
    text_primary=Colors.REBECCA_PURPLE,
    text_secondary=Colors.PURPLE,
    font_sans="Inter, system-ui, sans-serif",
    extra_tokens={
        "panel": Colors.DARK_GRAY,
        "panel_text": Colors.LIGHT_GRAY,
    },
)

stylesheet = GlobalStyleSheet(theme=css_theme)
cls_hero = stylesheet.add_class(
    "hero",
    Style(
        display=Display.FLEX,
        flex_direction=FlexDirection.COLUMN,
        align_items=Align.START,
        gap="16px",
        padding=EdgeInsets.symmetric(vertical=32, horizontal=24),
        border_radius="16px",
        background_color=css_theme.surface,
        color=css_theme.text_primary,
        border="1px solid rgba(255,255,255,0.08)",
    ),
)
cls_feature_grid = stylesheet.add_class(
    "feature-grid",
    Style(
        display=Display.GRID,
        gap="16px",
        grid_template_columns="repeat(auto-fit, minmax(220px, 1fr))",
    ),
)
cls_feature_card = stylesheet.add_class(
    "feature-card",
    Style(
        padding=EdgeInsets.all(32),
        border_radius="12px",
        background_color=css_theme.surface,
        color=css_theme.text_primary,
        border="1px solid rgba(255,255,255,0.10)",
    ),
)
cls_action_btn = stylesheet.add_class(
    "action-btn",
    Style(
        background_color=css_theme.surface,
        color=css_theme.text_primary,
        padding=EdgeInsets.symmetric(vertical=10, horizontal=18),
        border="none",
        border_radius="10px",
        font_weight="600",
        cursor="pointer",
        text_decoration="none",
        display=Display.INLINE_BLOCK,
    ),
)
stylesheet.add_raw(
    """
    .action-btn:hover { filter: brightness(1.08); transform: translateY(-1px); }
    .feature-card h2 { margin-bottom: 6px; }
    """
)
stylesheet.add_media_query(
    "(max-width: 768px)",
    {
        ".hero": Style(padding=EdgeInsets.symmetric(vertical=24, horizontal=16)),
        ".feature-grid": Style(grid_template_columns="1fr"),
        ".container": Style(padding="16px"),
    },
)
stylesheet.add_breakpoint(
    "sm",
    {
        ".action-btn": style(width="100%", text_align="center"),
    },
)

# Optional: register external assets for the document <head>
app.add_head_link(
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
)
app.add_head_script(
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
)


# 2. Define a reusable layout (functional component)
# This is equivalent to a React/Flutter-style component
def main_layout(page_title: str, children: Optional[list] = None) -> Html:
    return Html(
        children=[
            Head(children=[Title(children=[page_title]), stylesheet.render()]),
            Body(
                style=Style(
                    margin=EdgeInsets.all(0),
                    font_family=css_theme.font_sans,
                    background_color=css_theme.surface,
                    color=css_theme.text_secondary,
                ),
                children=[
                    Div(children=children, class_name="container py-5"),
                    # Footer
                    Div(
                        class_name="container py-4",
                        style=Style(
                            display=Display.FLEX,
                            justify_content=Align.SPACE_BETWEEN,
                            align_items=Align.CENTER,
                            color=css_theme.text_secondary,
                            background_color=css_theme.surface,
                            border_top="1px solid rgba(255,255,255,0.1)",
                        ),
                        children=[
                            Text("© 2026 Astris"),
                            Span(children=[f"Theme preset: {THEME_PRESET}"]),
                        ],
                    ),
                ]
            ),
        ]
    )


def post_template(entry: dict) -> Html:
    return main_layout(
        page_title=entry.get("title", "Post"),
        children=[
            Div(
                class_name="mb-4",
                children=[
                    A(
                        href="/posts",
                        class_name="text-decoration-none",
                        children=["← Back to posts"],
                    ),
                ],
            ),
            Div(
                class_name="mb-3",
                style=Style(
                    display=Display.FLEX,
                    flex_direction=FlexDirection.COLUMN,
                    gap="8px",
                    color=css_theme.text_secondary,
                ),
                children=[
                    H2(children=[entry.get("title", "Untitled")]),
                    P(style=Style(color=css_theme.text_secondary), children=[entry.get("summary", "")]),
                    P(
                        style=Style(color=css_theme.text_secondary),
                        children=[
                            f"By {entry.get('author', 'Unknown')} · {entry.get('published_at', 'Unknown date')}"
                        ],
                    ),
                ],
            ),
            P(children=[entry.get("content", "")]),
        ],
    )


posts_collection: JsonCollection = register_json_collection(
    app,
    name="posts",
    directory="content/posts",
    template=post_template,
    api_prefix="/api/collections",
)


# 3. Define pages (routes)


@app.page("/")
def home():

    return main_layout(
        page_title="Astris Showcase",
        children=[
            Section(
                class_name=cls_hero,
                children=[
                    H1(children=["Astris: Themes + Typed CSS + Reusable Classes"]),
                    P(
                        children=[
                            "This page demonstrates app themes, typed style objects, reusable CSS classes, and component composition in a single Python file."
                        ]
                    ),
                    Div(
                        style=style(display=Display.FLEX, gap="10px"),
                        children=[
                            A(href="/posts", class_name=cls_action_btn, children=["Browse posts"]),
                            Button(
                                class_name=cls_action_btn,
                                style=Style(
                                    background_color=css_theme.surface,
                                    color=css_theme.text_secondary,
                                ),
                                children=["Secondary action"],
                            ),
                        ],
                    ),
                ],
            ),
            Section(
                style=Style(margin=EdgeInsets.only(top=20)),
                children=[
                    H2(children=["Feature Cards"]),
                    Div(
                        class_name=cls_feature_grid,
                        children=[
                            Div(
                                class_name=cls_feature_card,
                                children=[
                                    H2(children=["Typed Style"]),
                                    P(children=["Use enums and EdgeInsets to avoid CSS typos."]),
                                ],
                            ),
                            Div(
                                class_name=cls_feature_card,
                                children=[
                                    H2(children=["Theme Tokens"]),
                                    P(children=["Consume design tokens through CSS variables."]),
                                ],
                            ),
                            Div(
                                class_name=cls_feature_card,
                                children=[
                                    H2(children=["GlobalStyleSheet"]),
                                    P(children=["Reuse class names instead of duplicating inline styles."]),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


@app.page("/posts")
def posts_index():
    return main_layout(
        page_title="Posts",
        children=[
            H2(children=["Posts"]),
            P(children=["These links are generated from JSON content files."]),
            Ul(
                style=Style(
                    display=Display.FLEX,
                    flex_direction=FlexDirection.COLUMN,
                    gap="8px",
                    list_style="none",
                    padding=EdgeInsets.all(0),
                ),
                children=[
                    Li(
                        children=[
                            A(
                                href=route,
                                class_name=cls_action_btn,
                                style=Style(
                                    background_color=css_theme.surface,
                                    color=css_theme.text_secondary,
                                ),
                                children=[route],
                            )
                        ]
                    )
                    for route in posts_collection.page_links()
                ],
            ),
        ],
    )


# 4. Entry point for UV/CLI
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        app.build()
    else:
        app.run_dev()
