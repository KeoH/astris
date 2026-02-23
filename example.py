import sys
from typing import Optional

# Simulate that astris is an installed package
from astris import Astris, Text, register_json_collection
from astris.content import JsonCollection
from astris.lib import A, Body, Div, H2, Head, Html, P, Title

# 1. Initialize the app
app = Astris()

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
            Head(children=[Title(children=[page_title])]),
            Body(
                children=[
                    Div(children=children, class_name="container py-5"),
                    # Footer
                    Div(
                        class_name="container py-4 text-secondary",
                        children=[Text("© 2026 Astris")],
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
                children=[
                    H2(children=[entry.get("title", "Untitled")]),
                    P(class_name="text-secondary", children=[entry.get("summary", "")]),
                    P(
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
        page_title="Welcome",
        children=[
            Div(
                class_name="mt-5",
                children=[
                    H2(children=["JSON content collection demo"]),
                    P(
                        children=[
                            "Astris is generating static pages from JSON files and exposing a read-only dev API."
                        ]
                    ),
                    A(
                        href="/posts",
                        class_name="btn btn-outline-primary",
                        children=["Browse posts"],
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
            Div(
                class_name="d-flex flex-column gap-2",
                children=[
                    A(href=route, children=[route])
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
