from __future__ import annotations

from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any, Dict, Literal, Mapping


_DEFAULT_LIGHT_COLORS: Dict[str, str] = {
    "bg": "#ffffff",
    "fg": "#0f172a",
    "surface": "#f8fafc",
    "surface-contrast": "#e2e8f0",
    "primary": "#2563eb",
    "primary-contrast": "#eff6ff",
    "muted": "#64748b",
}

_DEFAULT_DARK_COLORS: Dict[str, str] = {
    "bg": "#020617",
    "fg": "#e2e8f0",
    "surface": "#0f172a",
    "surface-contrast": "#1e293b",
    "primary": "#60a5fa",
    "primary-contrast": "#0f172a",
    "muted": "#94a3b8",
}

_DEFAULT_SPACING: Dict[str, str] = {
    "xs": "0.25rem",
    "sm": "0.5rem",
    "md": "1rem",
    "lg": "1.5rem",
    "xl": "2rem",
}

_DEFAULT_SCALES: Dict[str, Dict[str, str]] = {
    "radius": {
        "sm": "0.25rem",
        "md": "0.5rem",
        "lg": "0.75rem",
    },
    "font": {
        "sm": "0.875rem",
        "md": "1rem",
        "lg": "1.125rem",
        "xl": "1.25rem",
    },
}

_DEFAULT_COMPONENTS: Dict[str, Dict[str, str]] = {
    "body": {
        "style": "background: var(--color-bg); color: var(--color-fg);",
    },
    "Column": {
        "style": "display: flex; flex-direction: column; gap: var(--space-md, 1rem);",
    },
    "Row": {
        "style": "display: flex; flex-direction: row; gap: var(--space-md, 1rem);",
    },
}

_SOFT_LIGHT_COLORS: Dict[str, str] = {
    "bg": "#fdfaf6",
    "fg": "#2a2f3a",
    "surface": "#fff8ef",
    "surface-contrast": "#f4e9db",
    "primary": "#8b5cf6",
    "primary-contrast": "#f5f3ff",
    "muted": "#7a7f8f",
}

_SOFT_DARK_COLORS: Dict[str, str] = {
    "bg": "#16141f",
    "fg": "#f5f3ff",
    "surface": "#211d2f",
    "surface-contrast": "#2b2440",
    "primary": "#c4b5fd",
    "primary-contrast": "#2e1065",
    "muted": "#b9b0cf",
}

_SOFT_SPACING: Dict[str, str] = {
    "xs": "0.375rem",
    "sm": "0.625rem",
    "md": "1rem",
    "lg": "1.75rem",
    "xl": "2.5rem",
}


@dataclass(slots=True)
class Theme:
    """Configurable theme tokens and per-component defaults."""

    mode: str = "light"
    colors: Dict[str, str] = field(default_factory=dict)
    spacing: Dict[str, str] = field(default_factory=dict)
    scales: Dict[str, Dict[str, str]] = field(default_factory=dict)
    components: Dict[str, Dict[str, str]] = field(default_factory=dict)
    extras: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        normalized_mode = self.mode.lower().strip()
        if normalized_mode not in {"light", "dark"}:
            raise ValueError("Theme mode must be 'light' or 'dark'")
        self.mode = normalized_mode

        self.colors = dict(self.colors)
        self.spacing = dict(self.spacing)
        self.scales = {name: dict(values) for name, values in self.scales.items()}
        self.components = {
            key: dict(attributes) for key, attributes in self.components.items()
        }
        self.extras = dict(self.extras)

    @classmethod
    def from_dict(cls, config: Mapping[str, Any]) -> "Theme":
        """Create a theme from a generic mapping."""
        return cls(
            mode=str(config.get("mode", "light")),
            colors=dict(config.get("colors", {})),
            spacing=dict(config.get("spacing", {})),
            scales={
                str(name): dict(values)
                for name, values in dict(config.get("scales", {})).items()
            },
            components={
                str(name): dict(values)
                for name, values in dict(config.get("components", {})).items()
            },
            extras=dict(config.get("extras", {})),
        )

    def extend(self, **overrides: Any) -> "Theme":
        """Return a new Theme merged with partial overrides."""
        merged_scales = {
            name: dict(values) for name, values in self.scales.items()
        }
        merged_components = {
            name: dict(values) for name, values in self.components.items()
        }

        for scale_name, scale_values in dict(overrides.pop("scales", {})).items():
            existing = merged_scales.get(str(scale_name), {})
            existing.update(dict(scale_values))
            merged_scales[str(scale_name)] = existing

        for component_name, attrs in dict(overrides.pop("components", {})).items():
            existing = merged_components.get(str(component_name), {})
            existing.update(dict(attrs))
            merged_components[str(component_name)] = existing

        return Theme(
            mode=str(overrides.pop("mode", self.mode)),
            colors={**self.colors, **dict(overrides.pop("colors", {}))},
            spacing={**self.spacing, **dict(overrides.pop("spacing", {}))},
            scales=merged_scales,
            components=merged_components,
            extras={**self.extras, **dict(overrides.pop("extras", {}))},
        )

    def component_defaults(self, *keys: str) -> Dict[str, str]:
        """Return merged defaults for component keys (left to right)."""
        defaults: Dict[str, str] = {}
        for key in keys:
            values = self.components.get(key)
            if values:
                defaults.update(values)
        return defaults

    def to_css_variables(self) -> Dict[str, str]:
        """Convert theme tokens to CSS variable names."""
        variables: Dict[str, str] = {}

        for name, value in self.colors.items():
            variables[f"--color-{name}"] = value

        for name, value in self.spacing.items():
            variables[f"--space-{name}"] = value

        for scale_name, scale_values in self.scales.items():
            for token_name, value in scale_values.items():
                variables[f"--{scale_name}-{token_name}"] = value

        return variables

    def to_style_block(self) -> str:
        """Render a compact CSS block with root variables and color scheme."""
        variables = self.to_css_variables()
        declarations = [f"{name}: {value};" for name, value in variables.items()]
        declarations.append(f"color-scheme: {self.mode};")

        declarations_css = " ".join(declarations)
        return f":root {{ {declarations_css} }}"


_ACTIVE_THEME: ContextVar[Theme | None] = ContextVar("astris_active_theme", default=None)


def get_active_theme() -> Theme | None:
    """Return the active render-scoped theme."""
    return _ACTIVE_THEME.get()


def activate_theme(theme: Theme | None):
    """Set the active render-scoped theme and return context token."""
    return _ACTIVE_THEME.set(theme)


def deactivate_theme(token) -> None:
    """Restore previous theme context from token."""
    _ACTIVE_THEME.reset(token)


def create_default_theme(mode: Literal["light", "dark"] = "light") -> Theme:
    """Build Astris default theme preset for light or dark mode."""
    normalized_mode = mode.lower().strip()
    if normalized_mode not in {"light", "dark"}:
        raise ValueError("Theme mode must be 'light' or 'dark'")

    colors = _DEFAULT_DARK_COLORS if normalized_mode == "dark" else _DEFAULT_LIGHT_COLORS

    return Theme(
        mode=normalized_mode,
        colors=colors,
        spacing=_DEFAULT_SPACING,
        scales=_DEFAULT_SCALES,
        components=_DEFAULT_COMPONENTS,
        extras={"name": "astris-default"},
    )


def create_soft_theme(mode: Literal["light", "dark"] = "light") -> Theme:
    """Build Astris soft preset theme for light or dark mode."""
    normalized_mode = mode.lower().strip()
    if normalized_mode not in {"light", "dark"}:
        raise ValueError("Theme mode must be 'light' or 'dark'")

    colors = _SOFT_DARK_COLORS if normalized_mode == "dark" else _SOFT_LIGHT_COLORS

    base_theme = (
        create_default_theme("dark")
        if normalized_mode == "dark"
        else create_default_theme("light")
    )

    return base_theme.extend(
        colors=colors,
        spacing=_SOFT_SPACING,
        extras={"name": "astris-soft", "base": "astris-default"},
    )