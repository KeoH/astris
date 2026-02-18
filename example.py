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
                        style="padding: 20px; background: #eee;",
                        children=[
                            A(href="/", children=["Inicio"]),
                            Text(" | "),
                            A(href="/about", children=["Sobre Nosotros"]),
                        ],
                    ),
                    # Dynamic content
                    Container(style="padding: 20px;", children=[content_slot]),
                    # Footer
                    Div(
                        style="margin-top: 50px; color: #888;",
                        children=[Text("© 2024 Mi Framework Python")],
                    ),
                ]
            ),
        ]
    )


# 3. Define pages (routes)


@app.page("/")
def home():
    return main_layout(
        page_title="Bienvenido",
        content_slot=Column(
            children=[
                H1(children=["Hola, Mundo desde Python!"]),
                P(
                    children=[
                        "Este sitio fue generado sin escribir una sola línea de HTML puro."
                    ]
                ),
                A(href="/about", children=["Ir a About ->"]),
            ]
        ),
    )


@app.page("/about")
def about():
    features = ["Python Puro", "Hot Reload (vía FastAPI)", "Cero HTML"]

    return main_layout(
        page_title="Sobre Nosotros",
        content_slot=Column(
            children=[
                H1(children=["Acerca de este Framework!!"]),
                H2(children=["Características:"]),
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
