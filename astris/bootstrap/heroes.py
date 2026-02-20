from astris.component import Component

from ..lib import Div, Img, H1, P


class CenteredHero(Div):
    """A simple centered hero section with a title and description."""

    def __init__(
        self,
        title: str,
        description: str,
        logo_img_url: str,
        actions: list[Component] = [],
    ):
        super().__init__(
            class_name="px-4 py-5 my-5 text-center",
            children=[
                Img(
                    src=logo_img_url,
                    alt=title,
                    width="72",
                    height="57",
                    class_name="d-block mx-auto mb-4",
                ),
                H1(
                    children=[title],
                    class_name="display-5 fw-bold text-body-emphasis",
                ),
                Div(
                    class_name="col-lg-6 mx-auto",
                    children=[
                        P(description, class_name="lead mb-4"),
                        Div(
                            class_name="d-grid gap-2 d-sm-flex justify-content-sm-center mb-5",
                            children=actions,
                        ),
                    ],
                ),
            ],
        )
