import sys

# Simulate that astris is an installed package
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
def main_layout(page_title: str, content_slot):
    return Html(
        children=[
            Head(children=[Title(children=[page_title])]),
            Body(
                children=[
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
                    # Footer
                    Div(
                        class_name="container py-4 text-secondary",
                        children=[Text("© 2024 My Python Framework")],
                    ),
                ]
            ),
        ]
    )


# 3. Define pages (routes)


@app.page("/")
def home():
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
    )


# 4. Entry point for UV/CLI
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        app.build()
    else:
        app.run_dev()
