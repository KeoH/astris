from __future__ import annotations

from typing import Optional, Sequence

from astris import Component
from astris.lib import A, Button, Div, H1, H2, H3, Header, Img, Nav, P, Svg, Use


class BootstrapNavbar(Header):
    def __init__(self, brand: str, links: list[dict], **kwargs):
        super().__init__(
            class_name="border-bottom bg-white sticky-top",
            children=[
                Div(
                    class_name="container d-flex align-items-center justify-content-between py-3",
                    children=[
                        Div(
                            class_name="d-flex align-items-center gap-2",
                            children=[
                                Div("A", class_name="theme-brand-mark"),
                                A(brand, href="/", class_name="text-decoration-none fw-semibold text-dark"),
                            ],
                        ),
                        Nav(
                            class_name="d-flex gap-2",
                            children=[
                                A(
                                    item.get("label", "Link"),
                                    href=item.get("href", "#"),
                                    class_name=(
                                        "btn btn-sm "
                                        + ("btn-primary" if item.get("active") else "btn-outline-secondary")
                                    ),
                                )
                                for item in links
                            ],
                        ),
                    ],
                )
            ],
            **kwargs,
        )


class BootstrapBtn(Button):
    def __init__(self, text: str, variant: str = "primary", size: str = "md", **kwargs):
        size_class = ""
        if size == "sm":
            size_class = " btn-sm"
        elif size == "lg":
            size_class = " btn-lg"

        super().__init__(
            class_name=f"btn btn-{variant}{size_class}",
            children=[text],
            **kwargs,
        )


class CenteredHero(Div):
    """Centered hero section inspired by Bootstrap examples."""

    def __init__(
        self,
        title: str,
        description: str,
        logo_img_url: str,
        actions: Optional[Sequence[Component]] = None,
        **kwargs,
    ):
        action_nodes = list(actions) if actions is not None else []

        super().__init__(
            class_name="px-4 py-5 my-5 text-center theme-hero-art",
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
                    class_name="col-lg-8 mx-auto",
                    children=[
                        P(description, class_name="lead mb-4"),
                        Div(
                            class_name="d-grid gap-2 d-sm-flex justify-content-sm-center mb-2",
                            children=action_nodes,
                        ),
                    ],
                ),
            ],
            **kwargs,
        )


class IconFeature(Div):
    def __init__(
        self,
        icon_class: str,
        title: str,
        description: str,
        call_to_action: Optional[Sequence[Component]] = None,
    ) -> None:
        cta_nodes = list(call_to_action) if call_to_action is not None else []

        children: list[Component | str] = [
            Div(
                class_name="feature-icon d-inline-flex align-items-center justify-content-center text-bg-primary bg-gradient fs-2 mb-3 rounded-3 p-2",
                children=[
                    Svg(
                        class_name="bi",
                        width="1em",
                        height="1em",
                        aria_hidden="true",
                        children=[Use(xlink_href=f"#{icon_class}")],
                    )
                ],
            ),
            H3(class_name="fs-4 text-body-emphasis", children=[title]),
            P(children=[description]),
        ]
        children.extend(cta_nodes)

        super().__init__(
            class_name="feature col",
            children=children,
        )


class FeatureList(Div):
    def __init__(self, features: list[dict]) -> None:
        super().__init__(
            class_name="row g-4 py-4 row-cols-1 row-cols-md-2 row-cols-lg-3",
            children=[
                IconFeature(
                    icon_class=feature.get("icon_class", ""),
                    title=feature.get("title", ""),
                    description=feature.get("description", ""),
                    call_to_action=[
                        A(
                            class_name="icon-link text-decoration-none",
                            children=[feature.get("cta_label", "Learn more")],
                            href=feature.get("href", "#"),
                        )
                    ],
                )
                for feature in features
            ],
        )


class MarketingCard(Div):
    def __init__(self, title: str, description: str, **kwargs):
        super().__init__(
            class_name="card shadow-sm h-100",
            children=[
                Div(
                    class_name="card-body",
                    children=[
                        H2(title, class_name="h5 card-title"),
                        P(description, class_name="card-text text-secondary"),
                    ],
                )
            ],
            **kwargs,
        )
