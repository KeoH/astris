from astris.theme import Theme

from .stylesheet import stylesheet

BOOTSTRAP_CSS_CDN = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"

theme = Theme(
    mode="light",
    stylesheets=[BOOTSTRAP_CSS_CDN],
    stylesheet=stylesheet,
)

theme.scales = {
    "container": {
        "sm": "540px",
        "md": "720px",
        "lg": "960px",
        "xl": "1140px",
        "xxl": "1320px",
    },
    "radius": {
        "sm": "0.375rem",
        "md": "0.5rem",
        "lg": "0.75rem",
        "pill": "50rem",
    },
}

theme.colors = {
    "bg": "#f8f9fa",
    "surface": "#ffffff",
    "surface-strong": "#ffffff",
    "text": "#212529",
    "text-soft": "#6c757d",
    "border": "#dee2e6",
    "primary": "#0d6efd",
    "primary-strong": "#0b5ed7",
    "danger": "#dc3545",
    "danger-soft": "#f8d7da",
    "success": "#198754",
    "success-soft": "#d1e7dd",
    "warning": "#ffc107",
    "warning-soft": "#fff3cd",
    "info": "#0dcaf0",
    "info-soft": "#cff4fc",
}

theme.spacing = {
    "1": "0.25rem",
    "2": "0.5rem",
    "3": "1rem",
    "4": "1.5rem",
    "5": "3rem",
}

theme.extras = {
    "name": "astris-bootstrap",
    "base": "bootstrap-cdn",
}
