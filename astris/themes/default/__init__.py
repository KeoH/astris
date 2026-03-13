from astris.theme import Theme

from .stylesheet import stylesheet

theme = Theme(mode="light", stylesheet=stylesheet)

theme.scales = {
    "shadow": {
        "soft": "8px 8px 16px rgba(148, 163, 184, 0.18), -8px -8px 16px rgba(255, 255, 255, 0.85)",
        "soft-inset": "inset 4px 4px 8px rgba(148, 163, 184, 0.18), inset -4px -4px 8px rgba(255, 255, 255, 0.85)",
        "focus": "0 0 0 3px rgba(31, 111, 235, 0.2)",
    },
    "container": {
        "sm": "540px",
        "md": "768px",
        "lg": "1024px",
        "xl": "1180px",
    },
    "z": {
        "header": "40",
        "modal": "80",
        "overlay": "70",
    },
    "transition": {
        "fast": "160ms ease",
        "base": "220ms ease",
    },
    "font": {
        "sans": '"Manrope", "Avenir Next", "Segoe UI", sans-serif',
        "mono": '"JetBrains Mono", "SFMono-Regular", Consolas, monospace',
    },
    "radius": {
        "sm": "0.375rem",
        "md": "0.625rem",
        "lg": "0.9rem",
        "xl": "1.2rem",
        "pill": "999px",
    },
    "grid": {"gap": "1rem"},
}

theme.colors = {
    "bg": "#eef2f7",
    "surface": "#f6f8fc",
    "surface-strong": "#ffffff",
    "text": "#1f2a37",
    "text-soft": "#5f6c7b",
    "border": "#d8e0eb",
    "primary": "#1f6feb",
    "primary-strong": "#1558bc",
    "danger": "#cb3a31",
    "danger-soft": "#fde9e7",
    "success": "#1f9254",
    "success-soft": "#e7f7ee",
    "warning": "#b7791f",
    "warning-soft": "#fff5e6",
    "info": "#0f6ea6",
    "info-soft": "#e5f3fb",
}

theme.spacing = {
    "1": "0.25rem",
    "2": "0.5rem",
    "3": "0.75rem",
    "4": "1rem",
    "5": "1.25rem",
    "6": "1.5rem",
    "8": "2rem",
    "10": "2.5rem",
    "12": "3rem",
}
