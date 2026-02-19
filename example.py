import sys

# Simulate that astris is an installed package
from astris import AstrisApp, Text
from astris.layout import Column
from astris.bootstrap.heroes import CenteredHero
from astris.lib import Button, Html, Head, Body, Title, Div, Main

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
def main_layout(page_title: str):
    return Html(
        children=[
            Head(children=[Title(children=[page_title])]),
            Body(
                children=[
                    Main(
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
                        ]
                    ),
                    # Footer
                    Div(
                        class_name="container py-4 text-secondary",
                        children=[Text("© 2026 Astris")],
                    ),
                ]
            ),
        ]
    )


# 3. Define pages (routes)


@app.page("/")
def home():
    return main_layout(page_title="Welcome")


# 4. Entry point for UV/CLI
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        app.build()
    else:
        app.run_dev()
