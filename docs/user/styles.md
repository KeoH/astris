# Styles

`astris.styles` provides typed helpers for writing CSS declarations in Python.
This page shows practical examples for every class and constant currently available in `astris/styles.py`.

## Import everything you need

```python
from astris.styles import (
    Align,
    Colors,
    Display,
    EdgeInsets,
    FlexDirection,
    Position,
    PREDEFINED_BREAKPOINTS,
    Style,
    TextDecoration,
    TextDecorationLine,
    TextDecorationStyle,
    TextDecorationThickness,
    Theme,
    sx,
)
```

## Enums for safer CSS values

Use enums to avoid typos and get IDE completion.

```python
card_style = Style(
    display=Display.FLEX,
    flex_direction=FlexDirection.COLUMN,
    justify_content=Align.SPACE_BETWEEN,
    align_items=Align.CENTER,
    position=Position.RELATIVE,
    background_color=Colors.WHITE,
    color=Colors.BLACK,
)
```

## EdgeInsets

`EdgeInsets` helps with `padding` and `margin` shorthand values.

```python
all_sides = EdgeInsets.all(12)  # 12px
symmetric = EdgeInsets.symmetric(vertical=24, horizontal=16)  # 24px 16px
only_some = EdgeInsets.only(top=8, right=12, bottom=8, left=0)  # 8px 12px 8px 0px

box_style = Style(
    padding=all_sides,
    margin=symmetric,
)
```

## TextDecoration

`TextDecoration` builds the full `text-decoration` shorthand (`line`, `style`, `color`, `thickness`).

### Simple helpers

```python
link_style = Style(text_decoration=TextDecoration.underline())
muted_style = Style(text_decoration=TextDecoration.none())
```

### Full shorthand values

```python
fancy_link = Style(
    text_decoration=TextDecoration.underline(
        style=TextDecorationStyle.WAVY,
        color="rebeccapurple",
        thickness=2,
    )
)

warning_text = Style(
    text_decoration=TextDecoration.line_through(
        style=TextDecorationStyle.DOUBLE,
        color=Colors.BLACK,
        thickness="0.15em",
    )
)
```

### Multiple text-decoration lines

```python
combo = Style(
    text_decoration=TextDecoration.custom(
        line=[TextDecorationLine.UNDERLINE, TextDecorationLine.OVERLINE],
        style=TextDecorationStyle.DASHED,
        color="crimson",
        thickness=TextDecorationThickness.FROM_FONT,
    )
)
```

## Style base class

`Style` accepts known typed arguments and any additional CSS declaration in `snake_case`.

```python
button = Style(
    display=Display.INLINE_BLOCK,
    padding=EdgeInsets.symmetric(vertical=10, horizontal=18),
    border_radius="10px",
    box_shadow="0 6px 14px rgba(0,0,0,0.12)",
)

print(button.to_css())
# display: inline-block; padding: 10px 18px; border-radius: 10px; box-shadow: 0 6px 14px rgba(0,0,0,0.12);
```

## `sx(...)` shorthand and `Style.merge(...)`

```python
base = sx(display=Display.FLEX, gap="12px")
responsive = sx(gap="8px", align_items=Align.CENTER)

merged = Style.merge(
    base,
    responsive,
    justify_content=Align.SPACE_BETWEEN,
)
```

## Theme tokens for CSS variables

This `Theme` class belongs to `astris.styles` and is designed for CSS variable usage.

```python
theme = Theme.quick(
    name="brand-demo",
    brand_primary="#7c3aed",
    spacing_md="18px",
)

title_style = Style(
    color=theme.brand_primary,
    margin=EdgeInsets.only(bottom=theme.spacing_md),
)

print(theme.to_style_block())
# :root { --brand-primary: #7c3aed; --surface: #ffffff; ... }
```

## Predefined breakpoints

`PREDEFINED_BREAKPOINTS` exposes default responsive names used by stylesheet helpers.

```python
print(PREDEFINED_BREAKPOINTS["sm"])   # (max-width: 640px)
print(PREDEFINED_BREAKPOINTS["md"])   # (max-width: 768px)
print(PREDEFINED_BREAKPOINTS["lg"])   # (max-width: 1024px)
print(PREDEFINED_BREAKPOINTS["xl"])   # (max-width: 1280px)
print(PREDEFINED_BREAKPOINTS["2xl"])  # (max-width: 1536px)
```

For responsive class generation, see `GlobalStyleSheet` examples in [Themes](themes.md).