from __future__ import annotations

from typing import Dict, List

from .styles import PREDEFINED_BREAKPOINTS, Style, Theme


class GlobalStyleSheet:
    """Manage global CSS classes and raw blocks for optimized output."""

    def __init__(
        self, theme: Theme | None = None, breakpoints: Dict[str, str] | None = None
    ) -> None:
        self.theme = theme
        self._class_blocks: List[tuple[str, str]] = []
        self._raw_blocks: List[str] = []
        self._media_blocks: List[str] = []
        self._breakpoints: Dict[str, str] = {
            **PREDEFINED_BREAKPOINTS,
            **(breakpoints or {}),
        }

    def add_class(self, class_name: str, style: Style | str) -> str:
        declarations = style.to_css() if isinstance(style, Style) else str(style)
        self._class_blocks.append((class_name, declarations))
        return class_name

    def add_raw(self, css: str) -> None:
        self._raw_blocks.append(css)

    def add_media_query(self, query: str, rules: Dict[str, Style | str]) -> None:
        """Register responsive CSS rules under a media query."""
        blocks: List[str] = []
        for selector, style in rules.items():
            declarations = style.to_css() if isinstance(style, Style) else str(style)
            blocks.append(f"{selector} {{ {declarations} }}")

        media_block = f"@media {query} {{ {' '.join(blocks)} }}"
        self._media_blocks.append(media_block)

    def add_breakpoint(self, name: str, rules: Dict[str, Style | str]) -> None:
        """Register rules using a predefined breakpoint key."""
        if name not in self._breakpoints:
            available = ", ".join(sorted(self._breakpoints))
            raise ValueError(f"Unknown breakpoint '{name}'. Available: {available}")

        self.add_media_query(self._breakpoints[name], rules)

    def set_breakpoint(self, name: str, query: str) -> None:
        """Register or override a named breakpoint."""
        self._breakpoints[name] = query

    def get_breakpoints(self) -> Dict[str, str]:
        """Return configured breakpoints."""
        return dict(self._breakpoints)

    def render_css(self) -> str:
        blocks: List[str] = []

        if self.theme is not None:
            blocks.append(self.theme.to_style_block())

        for class_name, declarations in self._class_blocks:
            blocks.append(f".{class_name} {{ {declarations} }}")

        blocks.extend(self._media_blocks)

        blocks.extend(self._raw_blocks)
        return "\n".join(blocks)

    def render(self) -> str:
        return f"<style>{self.render_css()}</style>"
