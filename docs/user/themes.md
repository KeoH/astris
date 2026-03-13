# Themes

Astris themes are the base layer of your UI system. In practice, the recommended flow is:

1. Configure app-level tokens with `astris.theme.Theme`.
2. Create reusable classes with `StyleSheet`.
3. Compose routes using those classes and only use inline style for one-off adjustments.

The full working reference for this flow is `example.py`.

## Recommended workflow

### 1. Choose a preset and extend it

```python
from astris import Astris, create_default_theme, create_soft_theme

THEME_PRESET = "soft"

base_theme = (
    create_soft_theme("dark") if THEME_PRESET == "soft" else create_default_theme("dark")
)

theme = base_theme.extend(
    components={
        "body": {
            "style": "margin: 0; background: var(--color-bg); color: var(--color-fg);"
        },
        "Section": {
            "style": "margin-bottom: var(--space-lg);"
        },
    },
    extras={
        "global_css": [
            "* { box-sizing: border-box; }",
            "a { color: inherit; }",
        ]
    },
)

app = Astris(theme=theme)
```

### 2. Create reusable UI classes

```python
from astris.stylesheet import StyleSheet
from astris.styles import Display, EdgeInsets, FlexDirection, Style

stylesheet = StyleSheet()

cls_hero = stylesheet.add_class(
    "hero",
    Style(
        display=Display.FLEX,
        flex_direction=FlexDirection.COLUMN,
        gap="14px",
        padding=EdgeInsets.symmetric(vertical=28, horizontal=24),
        border_radius="16px",
        background_color="var(--color-surface)",
        border="1px solid var(--color-surface-contrast)",
    ),
)

cls_btn = stylesheet.add_class(
    "btn",
    Style(
        border="none",
        border_radius="10px",
        padding=EdgeInsets.symmetric(vertical=10, horizontal=16),
        background_color="var(--color-primary)",
        color="var(--color-primary-contrast)",
    ),
)

# Keep responsive overrides with the same class definition.
stylesheet.add_class(
    "page-shell",
    Style(padding="32px 20px"),
    responsive={"md": Style(padding="24px 14px")},
)
```

### 3. Attach stylesheet to the theme

```python
theme.set_stylesheet(stylesheet)
```

Astris auto-injects the generated class CSS in `<head>` when the stylesheet is attached to the active theme.

### 4. Use your normal layout

```python
from astris.components import Body, Head, Html, Title

def main_layout(page_title: str, children: list | None = None) -> Html:
    return Html(
        children=[
            Head(children=[Title(children=[page_title])]),
            Body(children=children or []),
        ]
    )
```

### 5. Use class names in routes

```python
from astris.components import A, Button, H1, P, Section

@app.page("/")
def home() -> Html:
    return main_layout(
        page_title="Astris Theme Guide",
        children=[
            Section(
                class_name=cls_hero,
                children=[
                    H1(children=["Astris themes in one file"]),
                    P(children=["Theme tokens + reusable classes + components."]),
                    A(href="/posts", class_name=cls_btn, children=["Browse posts"]),
                ],
            )
        ],
    )
```

## Use the default theme package

Astris includes a ready-to-use theme package in `astris.themes.default`.
It provides:

- a preconfigured `theme` object (tokens + stylesheet)
- a reusable HTML layout helper
- reusable UI components for common sections

### Minimal example with default theme components

```python
from astris import Astris
from astris.lib import Div, H1, P
from astris.themes.default import theme
from astris.themes.default.components import Badge, Btn, SimpleCard, SiteHeader, SiteNavbar
from astris.themes.default.layout import astris_ui_layout

app = Astris(theme=theme)


@app.page("/")
def home():
    navbar = SiteNavbar(
        options=[
            {"label": "Home", "href": "/", "active": True},
            {"label": "Themes", "href": "/themes"},
        ]
    )

    return astris_ui_layout(
        content=[
            SiteHeader("Astris", navbar),
            Div(
                class_name="container section stack-md fade-up",
                children=[
                    Badge("DEFAULT THEME", variant="primary"),
                    H1("Build pages with reusable themed components"),
                    P("Use the bundled layout, utilities, and semantic components."),
                    Btn("Read Docs", variant="primary"),
                    SimpleCard(
                        title="Fast start",
                        content="The default theme ships with card, button, badge, grid, and layout utilities.",
                    ),
                ],
            ),
        ]
    )
```

### Composed example with grid helpers

Use `Row` and `Col` helpers to build multi-column blocks with the default stylesheet classes.

```python
from astris import Astris
from astris.lib import Div, H2, P
from astris.themes.default import theme
from astris.themes.default.components import Col, Row, SimpleCard
from astris.themes.default.layout import astris_ui_layout

app = Astris(theme=theme)


@app.page("/features")
def features():
    return astris_ui_layout(
        content=[
            Div(
                class_name="container section stack-md",
                children=[
                    H2("Theme components in practice"),
                    P("Compose pages with predefined utility classes and themed components."),
                    Row(
                        children=[
                            Col(class_name="col-12 col-md-6 col-lg-4", children=[
                                SimpleCard("Tokens", "Use CSS variables generated by Theme.")
                            ]),
                            Col(class_name="col-12 col-md-6 col-lg-4", children=[
                                SimpleCard("Styles", "Use reusable class names from the default stylesheet.")
                            ]),
                            Col(class_name="col-12 col-md-6 col-lg-4", children=[
                                SimpleCard("Layout", "Use the bundled layout helper to keep page files small.")
                            ]),
                        ]
                    ),
                ],
            )
        ]
    )
```

### When to use package components vs custom classes

- Use package components (`Btn`, `Badge`, `SimpleCard`, `SiteHeader`) for common UI patterns.
- Use stylesheet utility classes (`container`, `section`, `stack-md`, `fade-up`) for page structure.
- Use custom `StyleSheet` classes when your project needs brand-specific variants.

## Use the ember-dark theme package

Astris also includes a dark preset package with deep red accents in `astris.themes.ember_dark`.

### Minimal example with ember-dark

```python
from astris import Astris
from astris.lib import Div, H1, P
from astris.themes.ember_dark import theme
from astris.themes.ember_dark.components import Badge, Btn, SiteHeader, SiteNavbar
from astris.themes.ember_dark.layout import astris_ui_layout

app = Astris(theme=theme)


@app.page("/")
def home():
    navbar = SiteNavbar(
        options=[
            {"label": "Home", "href": "/", "active": True},
            {"label": "Components", "href": "/components"},
        ]
    )

    return astris_ui_layout(
        content=[
            SiteHeader("Astris Ember", navbar),
            Div(
                class_name="container section stack-md fade-up",
                children=[
                    Badge("EMBER DARK", variant="primary"),
                    H1("Dark UI with deep red primary accents"),
                    P("Use ember-dark when you need a bold dark baseline out of the box."),
                    Btn("Explore", variant="primary"),
                ],
            ),
        ]
    )
```

## Use the bootstrap theme package

Astris includes a Bootstrap-based theme package in `astris.themes.bootstrap`.
It loads Bootstrap from CDN through `Theme.stylesheets` and adds Astris-native wrappers for hero, feature blocks, and navbar composition.

### Minimal example with bootstrap theme

```python
from astris import Astris
from astris.lib import Div
from astris.themes.bootstrap import theme
from astris.themes.bootstrap.components import BootstrapBtn, BootstrapNavbar, CenteredHero
from astris.themes.bootstrap.layout import bootstrap_layout

app = Astris(theme=theme)


@app.page("/")
def home():
    return bootstrap_layout(
        page_title="Astris Bootstrap",
        content=[
            BootstrapNavbar(
                brand="Astris",
                links=[
                    {"label": "Home", "href": "/", "active": True},
                    {"label": "Docs", "href": "https://astris.readthedocs.io"},
                ],
            ),
            Div(
                class_name="container py-5",
                children=[
                    CenteredHero(
                        title="Bootstrap + Astris components",
                        description="Use Bootstrap utility classes with composable Python components.",
                        logo_img_url="https://getbootstrap.com/docs/5.3/assets/brand/bootstrap-logo.svg",
                        actions=[BootstrapBtn("Get started", variant="primary")],
                    )
                ],
            ),
        ],
    )
```

## Theme token groups

- `colors`: exported as CSS variables `--color-*`
- `spacing`: exported as CSS variables `--space-*`
- `scales`: exported as CSS variables `--<scale>-<token>`
- `components`: default HTML attributes by component key
- `stylesheets`: external stylesheets to include in `<head>`
- `extras`: additional metadata and optional global CSS blocks

## Component defaults and precedence

Theme defaults are merged in this order:

1. Tag-level key (example: `"div"`)
2. Class-level key (example: `"Div"`)
3. Explicit attributes in component call

Explicit attributes always win.

Normalization rules:

- `class_name` becomes `class`
- `_` in attribute names becomes `-` (for example `data_variant` -> `data-variant`)

## Runtime behavior

When a theme is active, Astris injects in `<head>`:

- CSS variables generated from `colors`, `spacing`, and `scales`
- `color-scheme: <mode>`
- optional blocks from `extras["global_css"]`

Astris also injects `data-theme="<mode>"` into `<html>` if missing.

Theme resolution happens at render time, so you can switch themes before `run_dev()` responses or before `build()`.

## External stylesheets in Theme

You can register stylesheets directly in `Theme`:

- `Theme(stylesheets=[...])`
- `theme.add_stylesheet(href)`

Accepted formats:

- `https://...`
- `/...` (site-root path)
- relative paths such as `assets/base.css`

Non-HTTPS schemes are rejected.

## Tips for maintainable theming

- Keep reusable visual patterns in classes (`StyleSheet`).
- Use `Theme.components` for default attributes and low-level app defaults.
- Use inline `Style(...)` only for local one-off adjustments.
- Keep class names semantic (`hero`, `card`, `btn`) instead of route-specific names.

### Build behavior

`build()` keeps stylesheet links in generated HTML but does not copy local CSS files automatically.

If you use `/assets/base.css`, ensure your deployment serves that file path.

### Example 1: CDN base + theme tokens override

```python
from astris import Astris, Theme

app = Astris(
    theme=Theme(
        mode="light",
        stylesheets=["https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"],
        colors={"primary": "#7c3aed"},
    )
)
```

Use this when you want a mature CSS base and keep Astris theme tokens as your override layer.

### Example 2: Local base stylesheet for brand system

```python
from astris import Astris, Theme

app = Astris(
    theme=Theme(
        mode="dark",
        stylesheets=["/assets/brand-base.css"],
        colors={"bg": "#0f172a", "fg": "#e2e8f0"},
    )
)
```

This pattern is useful when your organization already owns a global CSS package.

### Example 3: Multiple external stylesheets

```python
from astris import Theme

theme = Theme(stylesheets=[
    "https://cdn.jsdelivr.net/npm/normalize.css@8.0.1/normalize.css",
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css",
    "/assets/app-base.css",
])
```

Order in the list is preserved and controls cascade between external files.

### Example 4: Add stylesheets incrementally

```python
from astris import Theme

theme = Theme(mode="light")
theme.add_stylesheet("https://cdn.example.com/base.css")
theme.add_stylesheet("/assets/layout.css")
```

This is practical when building theme setup across multiple modules.

### Example 5: Deduplication with `app.add_head_link(...)`

```python
from astris import Astris, Theme

app = Astris(theme=Theme(stylesheets=["https://cdn.example.com/base.css"]))

# Duplicate href: Astris keeps only one <link> for this href.
app.add_head_link("https://cdn.example.com/base.css")
app.add_head_link("https://cdn.example.com/overrides.css")
```

`base.css` appears once; `overrides.css` is added after theme CSS block.

### Example 6: Mixing theme stylesheets with runtime theme switching

```python
from astris import Astris, Theme

app = Astris(
    theme=Theme(
        mode="light",
        stylesheets=["/assets/base.css"],
        colors={"bg": "#ffffff", "fg": "#111827"},
    )
)

app.theme = Theme(
    mode="dark",
    stylesheets=["/assets/base.css"],
    colors={"bg": "#020617", "fg": "#e2e8f0"},
)
```

Shared external CSS can remain stable while mode tokens change.

### Example 7: Query/hash in stylesheet URL

```python
from astris import Theme

theme = Theme(stylesheets=["https://cdn.example.com/theme.css?v=2026-03-08#core"])
```

The full `href` string is used for deduplication.

### Example 8: Accepted stylesheet path formats

```python
from astris import Theme

# All of these are valid
theme = Theme(stylesheets=["assets/base.css"])
theme.add_stylesheet("/assets/layout.css")
theme.add_stylesheet("https://cdn.example.com/base.css")
```

### Troubleshooting

- Stylesheet not applied in static build:
  - Confirm the file is actually served at `/assets/...` by your hosting setup.
- Unexpected overrides:
  - Check order: theme external -> theme generated -> app head links.
- Duplicate links in source config:
  - Verify exact `href` strings (including query/hash) because dedupe is string-based.
- Validation error for stylesheet path:
    - Use only `https://...`, `/...`, or relative paths.

## StyleSheet for reusable classes

`StyleSheet` lets you avoid repeating inline style payload across many components.

For an extensive class-first guide (variants, responsive classes, tokenized classes, pitfalls), see [Styles](styles.md).

```python
from astris.stylesheet import StyleSheet
from astris.components import Body, Div, Head, Html, Text
from astris.styles import Display, EdgeInsets, Style, Theme

theme = Theme(name="default", brand_color="#ff5722", surface="#ffffff")
stylesheet = StyleSheet(theme=theme)

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

theme = Theme(name="Catalog")
theme.set_stylesheet(stylesheet)
app = Astris(theme=theme)

page = Html(
    children=[
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

Use `StyleSheet.add_media_query(...)` to register responsive rules in Python.

```python
from astris.stylesheet import StyleSheet
from astris.styles import EdgeInsets, Style

stylesheet = StyleSheet()

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
- Group related routes in dedicated router modules (for example `routes/pages.py`, `routes/posts.py`) and include them in the app entrypoint.
- Keep page files focused on structure and data flow.
