import sys

from astris import Astris, register_json_collection
from astris.content import JsonCollection
from astris.lib import A, Body, Div, H1, H2, Head, Html, Li, Meta, P, Section, Span, Title, Ul
from astris.styles import Display, EdgeInsets, Style
from astris.themes.ember_dark import theme
from astris.themes.ember_dark.components import Badge, Btn, Col, Row, SimpleCard, SiteHeader, SiteNavbar

app = Astris(theme=theme)


def app_shell(page_title: str, active_nav: str, content: list) -> Html:
    navbar = SiteNavbar(
        options=[
            {"label": "Home", "href": "/", "active": active_nav == "home"},
            {"label": "Showcase", "href": "/showcase", "active": active_nav == "showcase"},
            {"label": "Posts", "href": "/posts", "active": active_nav == "posts"},
        ]
    )

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
                children=[
                    SiteHeader("Astris Ember Studio", navbar),
                    Div(
                        class_name="container section stack-lg",
                        children=content,
                    ),
                    Div(
                        class_name="container section",
                        children=[
                            Div(
                                class_name="surface d-flex justify-between item-center",
                                children=[
                                    Span("Built with astris.themes.ember_dark"),
                                    Span("Mode: dark / Accent: deep red"),
                                ],
                            )
                        ],
                    ),
                ]
            ),
        ]
    )


def post_template(entry: dict) -> Html:
    return app_shell(
        page_title=entry.get("title", "Post"),
        active_nav="posts",
        content=[
            Badge("POST", variant="primary"),
            Div(
                class_name="surface stack-md",
                children=[
                    H1(entry.get("title", "Untitled")),
                    P(entry.get("summary", "")),
                    P(
                        f"By {entry.get('author', 'Unknown')} • {entry.get('published_at', 'Unknown date')}",
                        class_name="mono",
                    ),
                    P(entry.get("content", "")),
                ],
            ),
            A("Back to all posts", href="/posts", class_name="btn btn-secondary"),
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
    return app_shell(
        page_title="Astris Ember Studio",
        active_nav="home",
        content=[
            Div(
                class_name="surface stack-md fade-up",
                children=[
                    Badge("EMBER DARK", variant="primary"),
                    H1("A dramatic dark baseline for Astris projects"),
                    P(
                        "This example is rebuilt from scratch to showcase the ember_dark theme package, semantic components, and utility classes."
                    ),
                    Div(
                        class_name="d-flex gap-4 flex-wrap",
                        children=[
                            A("Open showcase", href="/showcase", class_name="btn btn-primary"),
                            A("Read generated posts", href="/posts", class_name="btn btn-secondary"),
                        ],
                    ),
                ],
            ),
            Row(
                children=[
                    Col(
                        class_name="col-12 col-md-6 col-lg-4",
                        children=[
                            SimpleCard(
                                title="Token-first",
                                content="Colors, spacing and scales come from ember_dark theme variables.",
                            )
                        ],
                    ),
                    Col(
                        class_name="col-12 col-md-6 col-lg-4",
                        children=[
                            SimpleCard(
                                title="Component-ready",
                                content="Use SiteHeader, SiteNavbar, Badge, Btn, Row and Col out of the box.",
                            )
                        ],
                    ),
                    Col(
                        class_name="col-12 col-md-6 col-lg-4",
                        children=[
                            SimpleCard(
                                title="Build-friendly",
                                content="Works in run_dev and static build with no extra theme wiring.",
                            )
                        ],
                    ),
                ]
            ),
        ],
    )


@app.page("/showcase")
def showcase() -> Html:
    return app_shell(
        page_title="Ember Showcase",
        active_nav="showcase",
        content=[
            Div(
                class_name="surface stack-md",
                children=[
                    Badge("SHOWCASE", variant="neutral"),
                    H2("Action states and semantic tones"),
                    P("Quick sample of ember_dark button and alert surfaces."),
                    Div(
                        class_name="d-flex gap-4 flex-wrap",
                        children=[
                            Btn("Primary", variant="primary"),
                            Btn("Secondary", variant="secondary"),
                            Btn("Danger", variant="danger"),
                            Btn("Ghost", variant="ghost"),
                        ],
                    ),
                ],
            ),
            Row(
                children=[
                    Col(
                        class_name="col-12 col-md-6",
                        children=[
                            Div(
                                class_name="alert alert-info",
                                children=[H2("Info"), P("Subtle cool tone for informative notes.")],
                            )
                        ],
                    ),
                    Col(
                        class_name="col-12 col-md-6",
                        children=[
                            Div(
                                class_name="alert alert-danger",
                                children=[H2("Danger"), P("Ember-dark keeps error messaging vivid and readable.")],
                            )
                        ],
                    ),
                ]
            ),
        ],
    )


@app.page("/posts")
def posts_index() -> Html:
    return app_shell(
        page_title="Generated Posts",
        active_nav="posts",
        content=[
            Badge("CONTENT", variant="success"),
            Section(
                class_name="surface stack-md",
                children=[
                    H2("JSON-backed pages"),
                    P("These links are generated from files in content/posts."),
                    Ul(
                        class_name="stack-sm",
                        style=Style(
                            list_style="none",
                            padding=EdgeInsets.all(0),
                            margin=EdgeInsets.all(0),
                            display=Display.GRID,
                            gap="var(--space-2)",
                        ),
                        children=[
                            Li(
                                children=[
                                    A(route, href=route, class_name="btn btn-secondary btn-block")
                                ]
                            )
                            for route in posts_collection.page_links()
                        ],
                    ),
                ],
            ),
        ],
    )


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        app.build()
    else:
        app.run_dev()
