from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Sequence, Union


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

    def __init__(
        self, children: Optional[Sequence[Union[Component, str]]] = None, **attributes
    ):
        self.children: List[Union[Component, str]] = list(children) if children else []
        self.attributes = self._process_attributes(attributes)

    def _process_attributes(self, attrs: Dict) -> Dict:
        processed = {}
        for key, value in attrs.items():
            normalized_key = key.replace("class_name", "class").replace("_", "-")
            processed[normalized_key] = value
        return processed

    def render(self) -> str:
        attrs_str = " ".join([f'{k}="{v}"' for k, v in self.attributes.items()])
        attrs_str = f" {attrs_str}" if attrs_str else ""

        children_html = ""
        for child in self.children:
            if isinstance(child, Component):
                children_html += child.render()
            else:
                children_html += str(child)

        return f"<{self.tag}{attrs_str}>{children_html}</{self.tag}>"
