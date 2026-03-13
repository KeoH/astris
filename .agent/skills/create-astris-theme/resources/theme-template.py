"""Starter template for creating a new Astris theme package."""

from astris.theme import Theme

from .stylesheet import stylesheet


theme = Theme(mode="light", stylesheet=stylesheet)

theme.scales = {
    "shadow": {
        "soft": "0 8px 20px rgba(0, 0, 0, 0.12)",
    },
    "radius": {
        "md": "0.625rem",
        "pill": "999px",
    },
}

theme.colors = {
    "bg": "#f8fafc",
    "surface": "#ffffff",
    "text": "#0f172a",
    "text-soft": "#475569",
    "border": "#e2e8f0",
    "primary": "#2563eb",
    "primary-strong": "#1d4ed8",
}

theme.spacing = {
    "2": "0.5rem",
    "4": "1rem",
    "6": "1.5rem",
    "10": "2.5rem",
}
