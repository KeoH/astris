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
        kwargs.setdefault(
            "style",
            "display: flex; flex-direction: column; gap: var(--space-md, 1rem);",
        )
        super().__init__(
            children,
            **kwargs,
        )


class Row(Div):
    """Convenience wrapper that applies a horizontal flex layout."""

    def __init__(
        self, children: Optional[Sequence[Component | str]] = None, **kwargs
    ) -> None:
        kwargs.setdefault(
            "style",
            "display: flex; flex-direction: row; gap: var(--space-md, 1rem);",
        )
        super().__init__(
            children,
            **kwargs,
        )
