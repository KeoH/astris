# Styles

`astris.styles` gives you typed CSS building blocks, and `astris.css_generator.GlobalStyleSheet` lets you convert those styles into reusable CSS classes.

This page is focused on a class-first workflow: define classes once, reuse them across many components.

## Choose the right Theme class

Astris currently has two different `Theme` classes:

- `astris.theme.Theme`: app-level theme for render-time defaults and theme mode.
- `astris.styles.Theme`: token-based helper for CSS variables in `GlobalStyleSheet`.

In this page, examples that generate classes use `astris.styles.Theme`.

## Recommended imports for class generation

```python
from astris.css_generator import GlobalStyleSheet
from astris.styles import (
    Align,
    Colors,
    Display,
    EdgeInsets,
    PREDEFINED_BREAKPOINTS,
    Style,
    TextDecoration,
    TextDecorationStyle,
    Theme,
    style,
)
```

## Quick start: register and reuse classes

```python
from astris.css_generator import GlobalStyleSheet
from astris.lib import Div
from astris.styles import Display, EdgeInsets, Style

stylesheet = GlobalStyleSheet()

card_class = stylesheet.add_class(
    "card",
    Style(
        display=Display.FLEX,
        flex_direction="column",
        gap="12px",
        padding=EdgeInsets.all(16),
        border_radius="12px",
        border="1px solid #e5e7eb",
        background_color="#ffffff",
    ),
)

card = Div(class_name=card_class, children=["Reusable card"])
```

`add_class(...)` returns the class name, so you can keep class names centralized and avoid hardcoded strings in page code.

## Compose class declarations with `Style` and `style(...)`

Use `Style(...)` for explicit, typed declarations.

```python
base_button = Style(
    display=Display.INLINE_BLOCK,
    padding=EdgeInsets.symmetric(vertical=10, horizontal=18),
    border_radius="10px",
    font_weight="600",
)
```

Use `style(...)` as shorthand where you do not need a long constructor.

```python
hover_ready = style(cursor="pointer", transition="all 120ms ease")
```

Merge both with `Style.merge(...)`.

```python
button_style = Style.merge(
    base_button,
    hover_ready,
    background_color=Colors.BLACK,
    color=Colors.WHITE,
)
```

## Build variants from shared base styles

```python
from astris.css_generator import GlobalStyleSheet
from astris.styles import Colors, EdgeInsets, Style

stylesheet = GlobalStyleSheet()

base_badge = Style(
    padding=EdgeInsets.symmetric(vertical=4, horizontal=10),
    border_radius="999px",
    font_size="12px",
    font_weight="600",
)

badge_success = stylesheet.add_class(
    "badge-success",
    Style.merge(base_badge, background_color="#ecfdf5", color="#065f46"),
)

badge_warning = stylesheet.add_class(
    "badge-warning",
    Style.merge(base_badge, background_color="#fffbeb", color="#92400e"),
)
```

## Use design tokens (`astris.styles.Theme`) in class generation

```python
from astris.css_generator import GlobalStyleSheet
from astris.styles import EdgeInsets, Style, Theme

tokens = Theme.quick(
    name="brand",
    brand_primary="#7c3aed",
    surface="#ffffff",
    text_primary="#111827",
    spacing_md="16px",
)

stylesheet = GlobalStyleSheet(theme=tokens)

stylesheet.add_class(
    "btn-brand",
    Style(
        background_color=tokens.brand_primary,
        color=tokens.surface,
        padding=EdgeInsets.symmetric(vertical=tokens.spacing_md, horizontal="20px"),
        border="none",
    ),
)
```

`GlobalStyleSheet(theme=tokens)` emits `:root` CSS variables automatically before class blocks.

## Responsive classes with media queries

```python
from astris.css_generator import GlobalStyleSheet
from astris.styles import Style

stylesheet = GlobalStyleSheet()

stylesheet.add_class(
    "feature-grid",
    Style(display="grid", gap="24px", grid_template_columns="repeat(3, 1fr)"),
)

stylesheet.add_media_query(
    "(max-width: 768px)",
    {
        ".feature-grid": Style(grid_template_columns="1fr", gap="12px"),
    },
)
```

Rules in `add_media_query(...)` are selector-based, so keys should include `.` for classes.

## Responsive classes with named breakpoints

`GlobalStyleSheet` includes predefined names from `PREDEFINED_BREAKPOINTS`.

```python
from astris.css_generator import GlobalStyleSheet
from astris.styles import EdgeInsets, Style

stylesheet = GlobalStyleSheet()

stylesheet.add_breakpoint(
    "md",
    {
        ".page-shell": Style(padding=EdgeInsets.symmetric(vertical=16, horizontal=12)),
        ".sidebar": Style(display="none"),
    },
)
```

You can define your own breakpoint names.

```python
stylesheet.set_breakpoint("tablet", "(max-width: 900px)")
stylesheet.add_breakpoint("tablet", {".hero-title": Style(font_size="1.5rem")})
```

## Add pseudo-selectors and advanced CSS

Use `add_raw(...)` for selectors that are not class declarations (`:hover`, `@keyframes`, feature queries).

```python
stylesheet.add_raw(".btn-brand:hover { filter: brightness(0.94); }")
stylesheet.add_raw("@keyframes fade-in { from { opacity: 0; } to { opacity: 1; } }")
stylesheet.add_raw(".fade-in { animation: fade-in 220ms ease-out; }")
```

## Inject the generated stylesheet into your page

```python
from astris import Astris, Text
from astris.css_generator import GlobalStyleSheet
from astris.lib import Body, Div, Head, Html
from astris.styles import EdgeInsets, Style

app = Astris()

stylesheet = GlobalStyleSheet()
card_class = stylesheet.add_class(
    "card",
    Style(padding=EdgeInsets.all(16), border="1px solid #e5e7eb", border_radius="12px"),
)


@app.page("/")
def home():
    return Html(
        children=[
            Head(children=[Text(stylesheet.render())]),
            Body(children=[Div(class_name=card_class, children=["Hello classes"])])
        ]
    )
```

For large apps, define stylesheet setup in a dedicated module and reuse exported class constants.

## Class-generation checklist

- Register classes with `add_class(...)` and reuse returned names.
- Use `Style.merge(...)` for variants instead of duplicating declarations.
- Put responsive overrides in `add_media_query(...)`/`add_breakpoint(...)`.
- Use `add_raw(...)` only for advanced selectors and at-rules.
- Keep class names stable (`card`, `btn-primary`, `feature-grid`) to simplify templates and tests.

## Common pitfalls

- Using relative selectors in media rules without prefix (`feature-grid` instead of `.feature-grid`).
- Expecting `GlobalStyleSheet` to auto-inject itself into `<head>` without `stylesheet.render()`.
- Mixing `astris.theme.Theme` and `astris.styles.Theme` in the same class-generation snippet.

For app-level theming and render-time defaults, see [Themes](themes.md).