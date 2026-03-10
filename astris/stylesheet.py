from __future__ import annotations

from typing import Dict, List, Mapping

from .styles import PREDEFINED_BREAKPOINTS, Style, Theme


class StyleSheet:
    """Manage global CSS classes and raw blocks for optimized output."""

    def __init__(
        self, theme: Theme | None = None, breakpoints: Dict[str, str] | None = None
    ) -> None:
        self.theme = theme
        self._class_blocks: List[tuple[str, str]] = []
        self._class_nested_blocks: List[str] = []
        self._raw_blocks: List[str] = []
        self._media_blocks: List[str] = []
        self._breakpoints: Dict[str, str] = {
            **PREDEFINED_BREAKPOINTS,
            **(breakpoints or {}),
        }

    def add_class(
        self,
        class_name: str,
        style: Style | str,
        responsive: Mapping[str, Style | str] | None = None,
    ) -> str:
        """Register a class with optional named-breakpoint responsive overrides."""
        base_selector = f".{class_name}"
        self._register_base_class(class_name, base_selector, style)
        self._register_responsive_classes(base_selector, responsive)
        return class_name

    @staticmethod
    def _style_to_css(style: Style | str) -> str:
        return style.to_css() if isinstance(style, Style) else str(style)

    @staticmethod
    def _nested_rule_blocks(selector: str, style: Style | str) -> List[str]:
        if not isinstance(style, Style):
            return []

        blocks: List[str] = []
        for nested_selector, declarations in style.nested_rules_for(selector):
            blocks.append(f"{nested_selector} {{ {declarations} }}")
        return blocks

    def _register_base_class(
        self, class_name: str, base_selector: str, style: Style | str
    ) -> None:
        declarations = self._style_to_css(style)
        if declarations.strip():
            self._class_blocks.append((class_name, declarations))
        self._class_nested_blocks.extend(self._nested_rule_blocks(base_selector, style))

    def _validate_breakpoint(self, breakpoint_name: str) -> str:
        if breakpoint_name not in self._breakpoints:
            available = ", ".join(sorted(self._breakpoints))
            raise ValueError(
                f"Unknown breakpoint '{breakpoint_name}'. Available: {available}"
            )
        return self._breakpoints[breakpoint_name]

    def _build_responsive_media_block(
        self, base_selector: str, breakpoint_name: str, style: Style | str
    ) -> str | None:
        media_query = self._validate_breakpoint(breakpoint_name)
        blocks: List[str] = []
        declarations = self._style_to_css(style)

        if declarations.strip():
            blocks.append(f"{base_selector} {{ {declarations} }}")

        blocks.extend(self._nested_rule_blocks(base_selector, style))

        if not blocks:
            return None

        return f"@media {media_query} {{ {' '.join(blocks)} }}"

    def _register_responsive_classes(
        self,
        base_selector: str,
        responsive: Mapping[str, Style | str] | None,
    ) -> None:
        if not responsive:
            return

        for breakpoint_name, responsive_style in responsive.items():
            media_block = self._build_responsive_media_block(
                base_selector, breakpoint_name, responsive_style
            )
            if media_block is not None:
                self._media_blocks.append(media_block)

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

        blocks.extend(self._class_nested_blocks)

        blocks.extend(self._media_blocks)

        blocks.extend(self._raw_blocks)
        return "\n".join(blocks)

    def render(self) -> str:
        return f"<style>{self.render_css()}</style>"
