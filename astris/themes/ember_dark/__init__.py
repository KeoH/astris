from astris.theme import Theme

from .stylesheet import stylesheet

theme = Theme(mode="dark", stylesheet=stylesheet)

theme.scales = {
    "shadow": {
        "soft": "0 18px 36px rgba(7, 8, 12, 0.45)",
        "soft-inset": "inset 0 1px 0 rgba(255, 255, 255, 0.03), inset 0 -1px 0 rgba(0, 0, 0, 0.5)",
        "focus": "0 0 0 3px rgba(139, 30, 45, 0.42)",
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
    "bg": "#0e0f14",
    "surface": "#161820",
    "surface-strong": "#1d202a",
    "text": "#f1f3f8",
    "text-soft": "#bcc3d3",
    "border": "#2a2f3c",
    "primary": "#8b1e2d",
    "primary-strong": "#b3263a",
    "danger": "#d14343",
    "danger-soft": "#3c1519",
    "success": "#2f9b65",
    "success-soft": "#113024",
    "warning": "#d49a35",
    "warning-soft": "#3a2a13",
    "info": "#4f8fcb",
    "info-soft": "#18283a",
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

theme.extras = {
    "name": "astris-ember-dark",
    "base": "astris-default",
}
