from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Mapping


PREDEFINED_BREAKPOINTS: Dict[str, str] = {
    "sm": "(max-width: 640px)",
    "md": "(max-width: 768px)",
    "lg": "(max-width: 1024px)",
    "xl": "(max-width: 1280px)",
    "2xl": "(max-width: 1536px)",
}


class Display(str, Enum):
    BLOCK = "block"
    INLINE = "inline"
    INLINE_BLOCK = "inline-block"
    FLEX = "flex"
    GRID = "grid"
    NONE = "none"


class FlexDirection(str, Enum):
    ROW = "row"
    ROW_REVERSE = "row-reverse"
    COLUMN = "column"
    COLUMN_REVERSE = "column-reverse"


class Align(str, Enum):
    START = "flex-start"
    END = "flex-end"
    CENTER = "center"
    STRETCH = "stretch"
    SPACE_BETWEEN = "space-between"
    SPACE_AROUND = "space-around"
    SPACE_EVENLY = "space-evenly"


class Position(str, Enum):
    STATIC = "static"
    RELATIVE = "relative"
    ABSOLUTE = "absolute"
    FIXED = "fixed"
    STICKY = "sticky"


class Colors(str, Enum):
    ALICE_BLUE = "aliceblue"
    ANTIQUE_WHITE = "antiquewhite"
    AQUA = "aqua"
    AQUAMARINE = "aquamarine"
    AZURE = "azure"
    BEIGE = "beige"
    BISQUE = "bisque"
    BLANCHED_ALMOND = "blanchedalmond"
    BLUE = "blue"
    BLUE_VIOLET = "blueviolet"
    BROWN = "brown"
    BURLY_WOOD = "burlywood"
    CADET_BLUE = "cadetblue"
    CHARTREUSE = "chartreuse"
    CHOCOLATE = "chocolate"
    CORAL = "coral"
    CORNFLOWER_BLUE = "cornflowerblue"
    CORNSILK = "cornsilk"
    CRIMSON = "crimson"
    CYAN = "cyan"
    DARK_BLUE = "darkblue"
    DARK_CYAN = "darkcyan"
    DARK_GOLDEN_ROD = "darkgoldenrod"
    DARK_GRAY = "darkgray"
    DARK_GREEN = "darkgreen"
    DARK_GREY = "darkgrey"
    DARK_KHAKI = "darkkhaki"
    DARK_MAGENTA = "darkmagenta"
    DARK_OLIVE_GREEN = "darkolivegreen"
    DARK_ORANGE = "darkorange"
    DARK_ORCHID = "darkorchid"
    DARK_RED = "darkred"
    DARK_SALMON = "darksalmon"
    DARK_SEA_GREEN = "darkseagreen"
    DARK_SLATE_BLUE = "darkslateblue"
    DARK_SLATE_GRAY = "darkslategray"
    DARK_SLATE_GREY = "darkslategrey"
    DARK_TURQUOISE = "darkturquoise"
    DARK_VIOLET = "darkviolet"
    DEEP_PINK = "deeppink"
    DEEP_SKY_BLUE = "deepskyblue"
    DIM_GRAY = "dimgray"
    DIM_GREY = "dimgrey"
    DODGER_BLUE = "dodgerblue"
    FIRE_BRICK = "firebrick"
    FLORAL_WHITE = "floralwhite"
    FOREST_GREEN = "forestgreen"
    FUCHSIA = "fuchsia"
    GAINSBORO = "gainsboro"
    GHOST_WHITE = "ghostwhite"
    GOLD = "gold"
    GOLDEN_ROD = "goldenrod"
    GRAY = "gray"
    GREEN = "green"
    GREEN_YELLOW = "greenyellow"
    GREY = "grey"
    HONEY_DEW = "honeydew"
    HOT_PINK = "hotpink"
    INDIAN_RED = "indianred"
    INDIGO = "indigo"
    IVORY = "ivory"
    KHAKI = "khaki"
    LAVENDER = "lavender"
    LAVENDER_BLUSH = "lavenderblush"
    LAWN_GREEN = "lawngreen"
    LEMON_CHIFFON = "lemonchiffon"
    LIGHT_BLUE = "lightblue"
    LIGHT_CORAL = "lightcoral"
    LIGHT_CYAN = "lightcyan"
    LIGHT_GOLDEN_ROD_YELLOW = "lightgoldenrodyellow"
    LIGHT_GRAY = "lightgray"
    LIGHT_GREEN = "lightgreen"
    LIGHT_GREY = "lightgrey"
    LIGHT_PINK = "lightpink"
    LIGHT_SALMON = "lightsalmon"
    LIGHT_SEA_GREEN = "lightseagreen"
    LIGHT_SKY_BLUE = "lightskyblue"
    LIGHT_SLATE_GRAY = "lightslategray"
    LIGHT_SLATE_GREY = "lightslategrey"
    LIGHT_STEEL_BLUE = "lightsteelblue"
    LIGHT_YELLOW = "lightyellow"
    LIME = "lime"
    LIME_GREEN = "limegreen"
    LINEN = "linen"
    MAGENTA = "magenta"
    MAROON = "maroon"
    MEDIUM_AQUA_MARINE = "mediumaquamarine"
    MEDIUM_BLUE = "mediumblue"
    MEDIUM_ORCHID = "mediumorchid"
    MEDIUM_PURPLE = "mediumpurple"
    MEDIUM_SEA_GREEN = "mediumseagreen"
    MEDIUM_SLATE_BLUE = "mediumslateblue"
    MEDIUM_SPRING_GREEN = "mediumspringgreen"
    MEDIUM_TURQUOISE = "mediumturquoise"
    MEDIUM_VIOLET_RED = "mediumvioletred"
    MIDNIGHT_BLUE = "midnightblue"
    MINT_CREAM = "mintcream"
    MISTY_ROSE = "mistyrose"
    MOCCASIN = "moccasin"
    NAVAJO_WHITE = "navajowhite"
    NAVY = "navy"
    OLD_LACE = "oldlace"
    OLIVE = "olive"
    OLIVE_DRAB = "olivedrab"
    ORANGE = "orange"
    ORANGE_RED = "orangered"
    ORCHID = "orchid"
    PALE_GOLDEN_ROD = "palegoldenrod"
    PALE_GREEN = "palegreen"
    PALE_TURQUOISE = "paleturquoise"
    PALE_VIOLET_RED = "palevioletred"
    PAPAYA_WHIP = "papayawhip"
    PEACH_PUFF = "peachpuff"
    PERU = "peru"
    PINK = "pink"
    PLUM = "plum"
    POWDER_BLUE = "powderblue"
    PURPLE = "purple"
    REBECCA_PURPLE = "rebeccapurple"
    RED = "red"
    ROSY_BROWN = "rosybrown"
    ROYAL_BLUE = "royalblue"
    SADDLE_BROWN = "saddlebrown"
    SALMON = "salmon"
    SANDY_BROWN = "sandybrown"
    SEA_GREEN = "seagreen"
    SEA_SHELL = "seashell"
    SIENNA = "sienna"
    SILVER = "silver"
    SKY_BLUE = "skyblue"
    SLATE_BLUE = "slateblue"
    SLATE_GRAY = "slategray"
    SLATE_GREY = "slategrey"
    SNOW = "snow"
    SPRING_GREEN = "springgreen"
    STEEL_BLUE = "steelblue"
    TAN = "tan"
    TEAL = "teal"
    THISTLE = "thistle"
    TOMATO = "tomato"
    TURQUOISE = "turquoise"
    VIOLET = "violet"
    WHEAT = "wheat"
    WHITE = "#ffffff"
    WHITE_SMOKE = "whitesmoke"
    BLACK = "#000000"
    YELLOW = "yellow"
    YELLOW_GREEN = "yellowgreen"
    TRANSPARENT = "transparent"


class TextDecorationLine(str, Enum):
    NONE = "none"
    UNDERLINE = "underline"
    OVERLINE = "overline"
    LINE_THROUGH = "line-through"
    BLINK = "blink"
    SPELLING_ERROR = "spelling-error"
    GRAMMAR_ERROR = "grammar-error"


class TextDecorationStyle(str, Enum):
    SOLID = "solid"
    DOUBLE = "double"
    DOTTED = "dotted"
    DASHED = "dashed"
    WAVY = "wavy"


class TextDecorationThickness(str, Enum):
    AUTO = "auto"
    FROM_FONT = "from-font"


def _to_css_size(value: str | int | float) -> str:
    if isinstance(value, (int, float)):
        return f"{value}px"
    return str(value)


@dataclass(frozen=True)
class EdgeInsets:
    top: str
    right: str
    bottom: str
    left: str

    @classmethod
    def all(cls, value: str | int | float) -> "EdgeInsets":
        css_value = _to_css_size(value)
        return cls(css_value, css_value, css_value, css_value)

    @classmethod
    def symmetric(
        cls,
        *,
        vertical: str | int | float = 0,
        horizontal: str | int | float = 0,
    ) -> "EdgeInsets":
        top_bottom = _to_css_size(vertical)
        left_right = _to_css_size(horizontal)
        return cls(top_bottom, left_right, top_bottom, left_right)

    @classmethod
    def only(
        cls,
        *,
        top: str | int | float = 0,
        right: str | int | float = 0,
        bottom: str | int | float = 0,
        left: str | int | float = 0,
    ) -> "EdgeInsets":
        return cls(
            _to_css_size(top),
            _to_css_size(right),
            _to_css_size(bottom),
            _to_css_size(left),
        )

    def to_css(self) -> str:
        if self.top == self.right == self.bottom == self.left:
            return self.top
        if self.top == self.bottom and self.right == self.left:
            return f"{self.top} {self.right}"
        return f"{self.top} {self.right} {self.bottom} {self.left}"

    def __str__(self) -> str:
        return self.to_css()


@dataclass(frozen=True)
class TextDecoration:
    line: tuple[str, ...] = ()
    style: str | None = None
    color: str | None = None
    thickness: str | None = None

    @classmethod
    def none(cls) -> "TextDecoration":
        return cls(line=(TextDecorationLine.NONE.value,))

    @classmethod
    def underline(
        cls,
        *,
        style: TextDecorationStyle | str | None = None,
        color: Colors | str | None = None,
        thickness: TextDecorationThickness | str | int | float | None = None,
    ) -> "TextDecoration":
        return cls.custom(
            line=TextDecorationLine.UNDERLINE,
            style=style,
            color=color,
            thickness=thickness,
        )

    @classmethod
    def overline(
        cls,
        *,
        style: TextDecorationStyle | str | None = None,
        color: Colors | str | None = None,
        thickness: TextDecorationThickness | str | int | float | None = None,
    ) -> "TextDecoration":
        return cls.custom(
            line=TextDecorationLine.OVERLINE,
            style=style,
            color=color,
            thickness=thickness,
        )

    @classmethod
    def line_through(
        cls,
        *,
        style: TextDecorationStyle | str | None = None,
        color: Colors | str | None = None,
        thickness: TextDecorationThickness | str | int | float | None = None,
    ) -> "TextDecoration":
        return cls.custom(
            line=TextDecorationLine.LINE_THROUGH,
            style=style,
            color=color,
            thickness=thickness,
        )

    @classmethod
    def custom(
        cls,
        *,
        line: TextDecorationLine
        | str
        | list[TextDecorationLine | str]
        | tuple[TextDecorationLine | str, ...]
        | None = None,
        style: TextDecorationStyle | str | None = None,
        color: Colors | str | None = None,
        thickness: TextDecorationThickness | str | int | float | None = None,
    ) -> "TextDecoration":
        return cls(
            line=cls._normalize_line(line),
            style=cls._serialize_optional(style),
            color=cls._serialize_optional(color),
            thickness=cls._serialize_thickness(thickness),
        )

    @staticmethod
    def _normalize_line(
        line: TextDecorationLine
        | str
        | list[TextDecorationLine | str]
        | tuple[TextDecorationLine | str, ...]
        | None,
    ) -> tuple[str, ...]:
        if line is None:
            return ()

        values: list[TextDecorationLine | str]
        if isinstance(line, (list, tuple)):
            values = list(line)
        else:
            values = [line]

        normalized: list[str] = []
        for value in values:
            if isinstance(value, Enum):
                normalized.append(str(value.value))
            else:
                normalized.append(str(value))
        return tuple(normalized)

    @staticmethod
    def _serialize_optional(value: Enum | str | None) -> str | None:
        if value is None:
            return None
        if isinstance(value, Enum):
            return str(value.value)
        return str(value)

    @staticmethod
    def _serialize_thickness(
        value: TextDecorationThickness | str | int | float | None,
    ) -> str | None:
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return _to_css_size(value)
        if isinstance(value, Enum):
            return str(value.value)
        return str(value)

    def to_css(self) -> str:
        parts: list[str] = []
        if self.line:
            parts.append(" ".join(self.line))
        if self.style is not None:
            parts.append(self.style)
        if self.color is not None:
            parts.append(self.color)
        if self.thickness is not None:
            parts.append(self.thickness)
        if not parts:
            return TextDecorationLine.NONE.value
        return " ".join(parts)

    def __str__(self) -> str:
        return self.to_css()


class Style:
    """Typed CSS declaration builder with enum, EdgeInsets and TextDecoration support."""

    def __init__(
        self,
        *,
        display: Display | str | None = None,
        flex_direction: FlexDirection | str | None = None,
        justify_content: Align | str | None = None,
        align_items: Align | str | None = None,
        position: Position | str | None = None,
        background_color: Colors | str | None = None,
        color: Colors | str | None = None,
        padding: EdgeInsets | str | int | float | None = None,
        margin: EdgeInsets | str | int | float | None = None,
        text_decoration: TextDecoration | str | None = None,
        states: Mapping[str, "Style | str"] | None = None,
        selectors: Mapping[str, "Style | str"] | None = None,
        **properties: Any,
    ) -> None:
        self._properties: Dict[str, str] = {}
        self._states: Dict[str, Style | str] = {}
        self._selectors: Dict[str, Style | str] = {}

        typed_props = {
            "display": display,
            "flex-direction": flex_direction,
            "justify-content": justify_content,
            "align-items": align_items,
            "position": position,
            "background-color": background_color,
            "color": color,
            "padding": padding,
            "margin": margin,
            "text-decoration": text_decoration,
        }

        for key, value in typed_props.items():
            if value is not None:
                self._properties[key] = self._serialize_value(value)

        for key, value in properties.items():
            if value is None:
                continue
            css_key = key.replace("_", "-")
            self._properties[css_key] = self._serialize_value(value)

        self._states = self._normalize_states(states)
        self._selectors = self._normalize_selectors(selectors)

    def _normalize_states(
        self, value: Mapping[str, "Style | str"] | None
    ) -> Dict[str, Style | str]:
        if not value:
            return {}

        normalized: Dict[str, Style | str] = {}
        for state_name, state_style in value.items():
            state_key = str(state_name).strip()
            if not state_key:
                continue

            if not state_key.startswith(":"):
                state_key = f":{state_key}"

            normalized[state_key] = state_style

        return normalized

    def _normalize_selectors(
        self, value: Mapping[str, "Style | str"] | None
    ) -> Dict[str, Style | str]:
        if not value:
            return {}

        normalized: Dict[str, Style | str] = {}
        for selector, selector_style in value.items():
            selector_key = str(selector).strip()
            if selector_key:
                normalized[selector_key] = selector_style

        return normalized

    def _serialize_value(self, value: Any) -> str:
        if isinstance(value, Enum):
            return str(value.value)
        if isinstance(value, EdgeInsets):
            return value.to_css()
        if isinstance(value, TextDecoration):
            return value.to_css()
        if isinstance(value, (int, float)):
            return str(value)
        return str(value)

    def to_css(self) -> str:
        declarations = [f"{key}: {value};" for key, value in self._properties.items()]
        return " ".join(declarations)

    def nested_rules_for(self, base_selector: str) -> list[tuple[str, str]]:
        """Return selector/declarations pairs for states and nested selectors."""
        rules: list[tuple[str, str]] = []

        for state_key, state_style in self._states.items():
            declarations = (
                state_style.to_css()
                if isinstance(state_style, Style)
                else str(state_style)
            ).strip()
            if declarations:
                rules.append((f"{base_selector}{state_key}", declarations))

        for selector_key, selector_style in self._selectors.items():
            declarations = (
                selector_style.to_css()
                if isinstance(selector_style, Style)
                else str(selector_style)
            ).strip()
            if not declarations:
                continue

            if "&" in selector_key:
                resolved_selector = selector_key.replace("&", base_selector)
            elif selector_key.startswith(":"):
                resolved_selector = f"{base_selector}{selector_key}"
            else:
                resolved_selector = f"{base_selector} {selector_key}"

            rules.append((resolved_selector, declarations))

        return rules

    @classmethod
    def merge(cls, *styles: "Style", **properties: Any) -> "Style":
        """Compose many Style objects and optional extra properties."""
        merged = cls(**properties)
        collected: Dict[str, str] = {}
        collected_states: Dict[str, Style | str] = {}
        collected_selectors: Dict[str, Style | str] = {}

        for style in styles:
            collected.update(style._properties)
            collected_states.update(style._states)
            collected_selectors.update(style._selectors)

        collected.update(merged._properties)
        collected_states.update(merged._states)
        collected_selectors.update(merged._selectors)
        merged._properties = collected
        merged._states = collected_states
        merged._selectors = collected_selectors
        return merged

    def __str__(self) -> str:
        return self.to_css()


class Theme:
    """Variable-based theme for typed style usage and global stylesheets."""

    def __init__(self, name: str = "default", **tokens: str) -> None:
        self.name = name
        self._tokens: Dict[str, str] = {
            key.replace("_", "-"): self._serialize_token(value)
            for key, value in tokens.items()
        }

    @staticmethod
    def _serialize_token(value: Any) -> str:
        if isinstance(value, Enum):
            return str(value.value)
        return str(value)

    @classmethod
    def quick(
        cls,
        name: str = "default",
        *,
        brand_primary: str = "#3B82F6",
        surface: str = "#ffffff",
        background: str = "#f8f9fa",
        text_primary: str = "#111827",
        text_secondary: str = "#6b7280",
        spacing_md: str = "16px",
        radius_md: str = "8px",
        font_sans: str = "Inter, system-ui, sans-serif",
        extra_tokens: Mapping[str, str] | None = None,
    ) -> "Theme":
        """Create a practical theme quickly with common design tokens."""
        base_tokens: Dict[str, str] = {
            "brand_primary": brand_primary,
            "surface": surface,
            "background": background,
            "text_primary": text_primary,
            "text_secondary": text_secondary,
            "spacing_md": spacing_md,
            "radius_md": radius_md,
            "font_sans": font_sans,
        }
        if extra_tokens:
            base_tokens.update(dict(extra_tokens))
        return cls(name=name, **base_tokens)

    def __getattr__(self, name: str) -> str:
        css_name = name.replace("_", "-")
        if css_name in self._tokens:
            return f"var(--{css_name})"
        raise AttributeError(f"Theme has no token '{name}'")

    def to_css_variables(self) -> Dict[str, str]:
        return {f"--{name}": value for name, value in self._tokens.items()}

    def to_style_block(self) -> str:
        variables = self.to_css_variables()
        declarations = " ".join(
            [f"{name}: {value};" for name, value in variables.items()]
        )
        return f":root {{ {declarations} }}"


def style(**properties: Any) -> Style:
    """Shorthand helper for Style creation."""
    return Style(**properties)
