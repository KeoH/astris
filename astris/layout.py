from typing import Optional, Sequence

from .component import Component
from .lib import Div


class Container(Div):
    """Convenience wrapper for a generic container block."""


class Column(Div):
    """Convenience wrapper that applies a vertical flex layout."""

    def __init__(
        self, children: Optional[Sequence[Component | str]] = None, **kwargs
    ) -> None:
        super().__init__(
            children, style="display: flex; flex-direction: column;", **kwargs
        )


class Row(Div):
    """Convenience wrapper that applies a horizontal flex layout."""

    def __init__(
        self, children: Optional[Sequence[Component | str]] = None, **kwargs
    ) -> None:
        super().__init__(
            children, style="display: flex; flex-direction: row;", **kwargs
        )
