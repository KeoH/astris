# Themes

Astris themes define design tokens and per-component default attributes.
When a theme is configured on `Astris`, it is applied during rendering in both `run_dev()` and `build()`.

Astris also supports typed CSS composition in Python through `astris.styles` and reusable class generation via `astris.css_generator.GlobalStyleSheet`.

## Typed styles with enums

```python
from astris.styles import Align, Colors, Display, EdgeInsets, FlexDirection, Position, Style
from astris.components import Div, Text

card = Div(
    style=Style(
        display=Display.FLEX,
        flex_direction=FlexDirection.COLUMN,
        justify_content=Align.SPACE_BETWEEN,
        align_items=Align.CENTER,
        position=Position.RELATIVE,
        background_color=Colors.WHITE,
        padding=EdgeInsets.all(24),
        margin=EdgeInsets.symmetric(vertical=16, horizontal="auto"),
        box_shadow="0px 10px 15px -3px rgba(0,0,0,0.1)",
        border_radius="12px",
    ),
    children=[Text("Typed style card")],
)
```

- Enum values provide safer style authoring and IDE completion.
- Unknown CSS properties are accepted as keyword arguments and converted from `snake_case` to `kebab-case`.

For quick style creation, use `sx(...)` as a shorthand:

```python
from astris.styles import Display, sx

inline = sx(display=Display.FLEX, gap="12px", align_items="center")
```

## EdgeInsets

```python
from astris.styles import EdgeInsets

padding_all = EdgeInsets.all(10)                       # 10px
margin_symmetric = EdgeInsets.symmetric(vertical=20, horizontal=15)  # 20px 15px
padding_only = EdgeInsets.only(top=10, bottom=5, left=20)            # 10px 0px 5px 20px
```

## Built-in presets

Astris includes two built-in preset factories:

- `create_default_theme(mode="light" | "dark")`
- `create_soft_theme(mode="light" | "dark")`

If you instantiate `Astris()` without passing `theme`, Astris automatically applies `create_default_theme("light")`.

```python
from astris import Astris, create_default_theme, create_soft_theme

app_auto = Astris()
app_default = Astris(theme=create_default_theme("light"))
app_soft = Astris(theme=create_soft_theme("dark"))
```

## Create a custom theme

You can define your own tokens and component defaults with `Theme(...)`.

```python
from astris import Astris, Theme

app = Astris(
    theme=Theme(
        mode="dark",
        colors={
            "bg": "#0f172a",
            "fg": "#e2e8f0",
            "primary": "#38bdf8",
        },
        spacing={
            "sm": "0.5rem",
            "md": "1rem",
            "lg": "1.5rem",
        },
        scales={
            "radius": {"sm": "0.25rem", "md": "0.5rem"},
            "font": {"md": "1rem", "lg": "1.125rem"},
        },
        components={
            "body": {"style": "background: var(--color-bg); color: var(--color-fg);"},
            "div": {"class_name": "surface"},
        },
        extras={
            "name": "brand-dark",
        },
    )
)
```

For a faster setup, use `Theme.quick(...)`:

```python
from astris.styles import Theme

theme = Theme.quick(
    name="demo",
    brand_primary="#7c3aed",
    text_primary="#f9fafb",
)
```

## Token groups

- `colors`: exported as CSS variables `--color-*`
- `spacing`: exported as CSS variables `--space-*`
- `scales`: exported as CSS variables `--<scale>-<token>`
- `components`: default HTML attributes by component key
- `extras`: arbitrary metadata (not exported as CSS variables)

## Component defaults and precedence

Theme component defaults are merged in this order:

1. Tag-level key (example: `"div"`)
2. Class-level key (example: `"Div"`)
3. Explicit attributes passed to the component

Explicit attributes always win.

```python
from astris import Theme
from astris.component import Element
from astris.theme import activate_theme, deactivate_theme


class Div(Element):
    tag = "div"


theme = Theme(
    components={
        "div": {"class_name": "surface", "id": "tag-id", "data_variant": "base"},
        "Div": {"id": "class-id", "data_density": "comfortable"},
    }
)

token = activate_theme(theme)
try:
    html = Div(
        children=["Hello"],
        class_name="hero",
        id="explicit-id",
    ).render()
finally:
    deactivate_theme(token)

print(html)
# <div class="hero" id="explicit-id" data-variant="base" data-density="comfortable">Hello</div>
```

Normalization rules also apply to theme defaults:

- `class_name` becomes `class`
- `_` in attribute names becomes `-` (for example `data_variant` -> `data-variant`)

## Runtime switching

Theme resolution happens at render time, so you can update `app.theme` before later renders/builds.

```python
from astris import Astris, Theme
from astris.lib import Div

app = Astris(theme=Theme(mode="light", components={"div": {"class_name": "light"}}))


@app.page("/")
def home():
    return Div(children=["Home"])


app.theme = Theme(mode="dark", components={"div": {"class_name": "dark"}})
app.build("dist")
```

## CSS variables and mode behavior

When `app.theme` is set, Astris injects a `<style>` block in `<head>` with:

- CSS variables generated from `colors`, `spacing`, and `scales`
- `color-scheme: <mode>`

Astris also injects `data-theme="<mode>"` into `<html>` if that attribute is missing.

## GlobalStyleSheet for reusable classes

`GlobalStyleSheet` lets you avoid repeating inline style payload across many components.

```python
from astris.css_generator import GlobalStyleSheet
from astris.components import Body, Div, Head, Html, Text
from astris.styles import Display, EdgeInsets, Style, Theme

theme = Theme(name="default", brand_color="#ff5722", surface="#ffffff")
stylesheet = GlobalStyleSheet(theme=theme)

btn = stylesheet.add_class(
    "btn-action",
    Style(
        background_color=theme.brand_color,
        color=theme.surface,
        padding=EdgeInsets.symmetric(vertical=12, horizontal=24),
        border="none",
        border_radius="6px",
        cursor="pointer",
    ),
)

grid = stylesheet.add_class(
    "product-grid",
    Style(
        display=Display.GRID,
        gap="24px",
        grid_template_columns="repeat(auto-fill, minmax(250px, 1fr))",
    ),
)

stylesheet.add_raw(
    """
    .btn-action:hover { filter: brightness(0.9); }
    """
)

stylesheet.add_media_query(
    "(max-width: 768px)",
    {
        ".product-grid": Style(grid_template_columns="1fr"),
        ".btn-action": Style(width="100%"),
    },
)

page = Html(
    children=[
        Head(children=[Text(stylesheet.render())]),
        Body(
            children=[
                Div(class_name=grid, children=[
                    Div(class_name=btn, children=["Item 1"]),
                    Div(class_name=btn, children=["Item 2"]),
                ])
            ]
        ),
    ]
)
```

For advanced selectors and keyframes, keep using `add_raw(...)`.

## Media queries (responsive design)

Use `GlobalStyleSheet.add_media_query(...)` to register responsive rules in Python.

```python
from astris.css_generator import GlobalStyleSheet
from astris.styles import EdgeInsets, Style

stylesheet = GlobalStyleSheet()

stylesheet.add_media_query(
    "(max-width: 768px)",
    {
        ".hero": Style(padding=EdgeInsets.symmetric(vertical=24, horizontal=16)),
        ".feature-grid": Style(grid_template_columns="1fr"),
        ".action-btn": Style(width="100%"),
    },
)
```

You can also use predefined breakpoint names with `add_breakpoint(...)`.

Built-in names:

- `sm` -> `(max-width: 640px)`
- `md` -> `(max-width: 768px)`
- `lg` -> `(max-width: 1024px)`
- `xl` -> `(max-width: 1280px)`
- `2xl` -> `(max-width: 1536px)`

```python
stylesheet.add_breakpoint(
    "md",
    {
        ".feature-grid": Style(grid_template_columns="1fr"),
        ".action-btn": Style(width="100%"),
    },
)

# Optional custom breakpoint
stylesheet.set_breakpoint("tablet", "(max-width: 900px)")
stylesheet.add_breakpoint("tablet", {".sidebar": Style(display="none")})
```

### How it works

- `query`: any valid media query condition string (for example `(max-width: 768px)`).
- `rules`: mapping of CSS selectors to either `Style(...)` or raw declaration strings.

Example mixing typed and raw declarations:

```python
stylesheet.add_media_query(
    "(max-width: 480px)",
    {
        ".layout": Style(gap="8px"),
        ".title": "font-size: 1.1rem; line-height: 1.3;",
    },
)
```

### Recommended responsive workflow

1. Define base desktop/tablet classes with `add_class(...)`.
2. Add one or more breakpoints with `add_media_query(...)`.
3. Use `add_raw(...)` for advanced patterns not covered by typed rules (`@keyframes`, complex pseudo-selectors, nested feature queries).

## Recommended project structure

- Keep theme tokens and global stylesheet setup in a dedicated module (for example `theme.py`).
- Register reusable classes close to domain components, not inside route handlers.
- Keep page files focused on structure and data flow.
