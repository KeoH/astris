import sys
from typing import Optional

# Simulate that astris is an installed package
<<<<<<< Updated upstream
from astris import AstrisApp, Text
from astris.lib import (
    Html,
    Head,
    Body,
    Title,
    Div,
    H1,
    H2,
    P,
    A,
    Ul,
    Li,
    Container,
    Column,
)
=======
from astris import AstrisApp, Text, register_json_collection
from astris.bootstrap.features import FeatureList
from astris.bootstrap.heroes import CenteredHero
from astris.lib import A, Body, Button, Div, H2, Head, Html, Main, P, Small, Title
>>>>>>> Stashed changes

# 1. Initialize the app
app = AstrisApp()

# Optional: register external assets for the document <head>
app.add_head_link(
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
)
app.add_head_script(
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
)


# 2. Define a reusable layout (functional component)
# This is equivalent to a React/Flutter-style component
<<<<<<< Updated upstream
def main_layout(page_title: str, content_slot):
=======
def main_layout(page_title: str, children: Optional[list] = None) -> Html:
>>>>>>> Stashed changes
    return Html(
        children=[
            Head(children=[Title(children=[page_title])]),
            Body(
                children=[
<<<<<<< Updated upstream
                    # Simple navbar
                    Div(
                        class_name="container py-3",
                        children=[
                            A(href="/", class_name="me-2", children=["Home"]),
                            Text(" | "),
                            A(href="/about", children=["About Us"]),
                        ],
                    ),
                    # Dynamic content
                    Container(class_name="container py-4", children=[content_slot]),
=======
                    Main(children=children, class_name="container py-5"),
>>>>>>> Stashed changes
                    # Footer
                    Div(
                        class_name="container py-4 text-secondary",
                        children=[Text("© 2024 My Python Framework")],
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
                    A(href="/posts", class_name="text-decoration-none", children=["← Back to posts"]),
                ],
            ),
            Div(
                class_name="mb-3",
                children=[
                    H2(children=[entry.get("title", "Untitled")]),
                    P(class_name="text-secondary", children=[entry.get("summary", "")]),
                    Small(
                        class_name="text-muted",
                        children=[
                            f"By {entry.get('author', 'Unknown')} · {entry.get('published_at', 'Unknown date')}"
                        ],
                    ),
                ],
            ),
            P(children=[entry.get("content", "")]),
        ],
    )


posts_collection = register_json_collection(
    app,
    name="posts",
    directory="content/posts",
    template=post_template,
    api_prefix="/api/collections",
)


# 3. Define pages (routes)


@app.page("/")
def home():
<<<<<<< Updated upstream
    return main_layout(
        page_title="Welcome",
        content_slot=Column(
            children=[
                H1(children=["Hello, World from Python!"]),
                P(
                    children=[
                        "This site was generated without writing a single line of raw HTML."
                    ]
                ),
                A(href="/about", children=["Go to About ->"]),
            ]
        ),
    )


@app.page("/about")
def about():
    features = ["Pure Python", "Hot Reload (via FastAPI)", "Zero HTML"]

    return main_layout(
        page_title="About Us",
        content_slot=Column(
            children=[
                H1(children=["About this Framework!!"]),
                H2(children=["Features:"]),
                Ul(
                    children=[
                        Li(children=[feat])
                        for feat in features  # List comprehension (Pythonic!)
                    ]
                ),
            ]
        ),
=======

    features = [
        {
            "icon_class": "collection",
            "title": "Feature 1",
            "description": "Description for feature 1.",
            "href": "#",
        },
        {
            "icon_class": "collection",
            "title": "Feature 2",
            "description": "Description for feature 2.",
            "href": "#",
        },
        {
            "icon_class": "collection",
            "title": "Feature 3",
            "description": "Description for feature 3.",
            "href": "#",
        },
    ]

    return main_layout(
        page_title="Welcome",
        children=[
            CenteredHero(
                title="Astris Framework",
                description="Build static sites with pure Python!",
                logo_img_url="https://getbootstrap.com/docs/5.3/assets/brand/bootstrap-logo.svg",
                actions=[
                    Button(
                        type="button",
                        class_name="btn btn-primary btn-lg px-4 gap-3",
                        children=["Get Started"],
                    ),
                    Button(
                        type="button",
                        class_name="btn btn-outline-secondary btn-lg px-4",
                        children=["Learn More"],
                    ),
                ],
            ),
            FeatureList(features=features),
            Div(
                class_name="mt-5",
                children=[
                    H2(children=["JSON content collection demo"]),
                    P(
                        children=[
                            "Astris is generating static pages from JSON files and exposing a read-only dev API."
                        ]
                    ),
                    A(href="/posts", class_name="btn btn-outline-primary", children=["Browse posts"]),
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
            Div(
                class_name="d-flex flex-column gap-2",
                children=[
                    A(href=route, children=[route])
                    for route in posts_collection.page_links()
                ],
            ),
        ],
>>>>>>> Stashed changes
    )


# 4. Entry point for UV/CLI
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        app.build()
    else:
        app.run_dev()
