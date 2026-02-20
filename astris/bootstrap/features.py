from typing import Optional

from astris.lib import Div, Svg, Use, H3, P, A

class FeatureList(Div):
    
    def __init__(self, features: list[dict]) -> None:
        super().__init__(
            class_name="row g-4 py-5 row-cols-1 row-cols-lg-3",
            children=[
                IconFeature(
                    icon_class=feature.get("icon_class", ""),
                    title=feature.get("title", ""),
                    description=feature.get("description", ""),
                    call_to_action=[
                        A(
                            class_name="icon-link",
                            children=["Learn More"],
                            href=feature.get("href", "#")
                        )
                    ],
                ) for feature in features
            ]
        )

class IconFeature(Div):

    def __init__(
        self,
        icon_class: str,
        title: str,
        description: str,
        call_to_action: Optional[list] = None,
    ) -> None:

        children = [
            Div(
                class_name="feature-icon d-inline-flex align-items-center justify-content-center text-bg-primary bg-gradient fs-2 mb-3",
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
            H3(class_name="fs-2 text-body-emphasis", children=[title]),
            P(children=[description])
        ]
        
        if call_to_action is not None:
            children.extend(call_to_action)

        super().__init__(
            class_name="feature col",
            children=children,
        )
