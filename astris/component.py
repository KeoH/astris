from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Sequence, Union

from .styles import Style

from .theme import get_active_theme


class Component(ABC):
    """Base class for all UI elements (widgets)."""

    @abstractmethod
    def render(self) -> str:
        pass

    def __str__(self):
        return self.render()


class Text(Component):
    """Render plain text without tags."""

    def __init__(self, content: str):
        self.content = content

    def render(self) -> str:
        return str(self.content)


class Element(Component):
    """
    Represents a generic HTML tag.
    Works like a Flutter-style container that accepts children.
    """

    tag: str = "div"
    VOID_TAGS = {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }

    def __init__(
        self, children: Optional[Sequence[Union[Component, str]]] = None, **attributes
    ):
        style = attributes.pop("style", None)
        styles = attributes.pop("styles", None)
        if "id" in attributes:
            self.id = attributes.get("id")

        normalized_styles: List[Style] = []
        if styles is not None:
            if isinstance(styles, Style):
                normalized_styles = [styles]
            else:
                normalized_styles = list(styles)

        self.children: List[Union[Component, str]] = list(children) if children else []
        self.attributes = self._process_attributes(attributes)
        if style is not None:
            if isinstance(style, Style):
                style = Style.merge(style, *normalized_styles)
                self.attributes["style"] = style.to_css()
            else:
                self.attributes["style"] = str(style)
        elif normalized_styles:
            style = Style.merge(*normalized_styles)
            self.attributes["style"] = style.to_css()

    def _process_attributes(self, attrs: Dict) -> Dict:
        processed = {}
        for key, value in attrs.items():
            normalized_key = key.replace("class_name", "class").replace("_", "-")
            processed[normalized_key] = value
        return processed

    def render(self) -> str:
        resolved_attributes = self._resolve_attributes()
        attrs_str = " ".join([f'{k}="{v}"' for k, v in resolved_attributes.items()])
        attrs_str = f" {attrs_str}" if attrs_str else ""

        if self.tag.lower() in self.VOID_TAGS:
            return f"<{self.tag}{attrs_str}>"

        children_html = ""
        for child in self.children:
            if isinstance(child, Component):
                children_html += child.render()
            else:
                children_html += str(child)

        return f"<{self.tag}{attrs_str}>{children_html}</{self.tag}>"

    def _resolve_attributes(self) -> Dict:
        theme = get_active_theme()
        if theme is None:
            return dict(self.attributes)

        theme_defaults = theme.component_defaults(
            self.tag.lower(), self.__class__.__name__
        )
        if not theme_defaults:
            return dict(self.attributes)

        normalized_defaults = self._process_attributes(theme_defaults)
        resolved_attributes = dict(normalized_defaults)
        resolved_attributes.update(self.attributes)
        return resolved_attributes
