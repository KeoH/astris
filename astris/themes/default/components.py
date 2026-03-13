from __future__ import annotations

from typing import Optional

from astris import Component
from astris.lib import (
    A,
    Article,
    Button,
    Div,
    P,
    H3,
    Header,
    Label,
    Nav,
    Option,
    Select,
    Span,
    Textarea,
    Input,
)


class Row(Div):
    def __init__(self, **kwargs):
        super().__init__(class_name="row", **kwargs)


class Col(Div):
    def __init__(self, class_name: str, **kwargs):
        super().__init__(class_name=class_name, **kwargs)


class SimpleCard(Article):
    def __init__(self, title: str, content: str, **kwargs):
        super().__init__(
            class_name="card",
            children=[
                H3(title, class_name="card-title"),
                P(content, class_name="card-content"),
            ],
            **kwargs,
        )


class SimpleSelect(Select):
    def __init__(self, options: list[dict], **kwargs):
        super().__init__(
            class_name="select",
            children=[Option(item["label"], value=item["value"]) for item in options],
            **kwargs,
        )


class Badge(Span):
    def __init__(self, text: str, variant: str = "neutral", **kwargs):
        super().__init__(class_name=f"badge badge-{variant}", children=[text], **kwargs)


class Btn(Button):
    def __init__(
        self,
        text: str,
        variant: str = "secondary",
        size: str = "md",
        is_loading: bool = False,
        is_disabled: bool = False,
        **kwargs,
    ):
        if size and size != "md":
            class_name = f"btn btn-{variant} btn-{size}"
        else:
            class_name = f"btn btn-{variant}"

        if is_loading:
            class_name += " is-loading"

        if is_disabled:
            kwargs["disabled"] = True

        super().__init__(class_name=class_name, children=[text], **kwargs)


class FormControl(Div):
    def __init__(
        self,
        label: str,
        input_element,
        children: Optional[list[Component]] = None,
        **kwargs,
    ):

        class_name = kwargs.get("class_name", "")

        full_children = [
            Label(label, class_name="label", for_=input_element.id),
            input_element,
        ]

        if children:
            full_children.extend(children)

        super().__init__(
            class_name=(
                "form-control" if not class_name else f"form-control {class_name}"
            ),
            children=full_children,
            **kwargs,
        )


class SimpleTextarea(Textarea):
    def __init__(self, **kwargs):
        class_name = kwargs.get("class_name", "")
        super().__init__(
            class_name="textarea" if not class_name else f"textarea {class_name}",
            **kwargs,
        )


class SimpleCheckbox(Label):

    def __init__(self, label: str, is_checked: bool = False, **kwargs):
        super().__init__(
            class_name="choice",
            children=[
                Input(checked=is_checked, type="checkbox"),
                label,
            ],
            **kwargs,
        )


class SimpleRadio(Label):
    def __init__(self, label: str, name: str, is_checked: bool = False, **kwargs):
        super().__init__(
            class_name="choice",
            children=[
                Input(checked=is_checked, type="radio", name=name),
                label,
            ],
            **kwargs,
        )


class SiteHeader(Header):
    def __init__(self, title: str, navbar_menu: SiteNavbar, **kwargs):
        super().__init__(
            class_name="site-header",
            children=[
                Div(
                    class_name="container navbar",
                    children=[
                        Div(title, class_name="brand"),
                        navbar_menu,
                    ],
                )
            ],
            **kwargs,
        )


class SiteNavbar(Nav):

    def __init__(self, options: list[dict], **kwargs):
        super().__init__(
            class_name="nav-links",
            children=[
                A(
                    option["label"],
                    href=option["href"],
                    class_name="nav-link"
                    + (" is-active" if option.get("active") else ""),
                )
                for option in options
            ],
            **kwargs,
        )
