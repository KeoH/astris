from astris import StyleSheet
from astris.styles import Align, Display, Style, Position

stylesheet = StyleSheet()


stylesheet.add_class(
    "site-header",
    style=Style(
        position=Position.STICKY,
        top="0",
        z_index="var(--z-header)",
        backdrop_filter="blur(8px)",
        background_color="rgba(14, 15, 20, 0.84)",
        border_bottom="1px solid rgba(42, 47, 60, 0.9)",
    ),
)

stylesheet.add_class(
    "navbar",
    style=Style(
        min_height="68px",
        display=Display.FLEX,
        align_items=Align.CENTER,
        justify_content=Align.SPACE_BETWEEN,
        gap="var(--space-4)",
    ),
    responsive={
        "md": Style(
            flex_direction="column",
            align_items=Align.START,
            padding_block="var(--space-3)",
        )
    },
)

stylesheet.add_class(
    "brand",
    style=Style(
        font_weight=800,
        letter_spacing="-0.02em",
        font_size="1.05rem",
        color="var(--color-text)",
    ),
)

stylesheet.add_class(
    "nav-links",
    style=Style(display=Display.FLEX, align_items=Align.CENTER, gap="var(--space-2)"),
)

stylesheet.add_class(
    "nav-link",
    style=Style(
        padding="0.45rem 0.75rem",
        border_radius="var(--radius-pill)",
        color="var(--color-text-soft)",
        font_weight=600,
    ),
)

nav_link_active_style = Style(
    color="var(--color-primary)",
    background_color="rgba(139, 30, 45, 0.16)",
    text_decoration="none",
)

stylesheet.add_class("nav-link:hover", style=nav_link_active_style)
stylesheet.add_class("nav-link.is-active", style=nav_link_active_style)

# Attribute selectors are added as raw CSS because add_class always prefixes a dot.
stylesheet.add_raw(
    """
[class*=\"col-\"] {
  width: 100%;
}
"""
)

for i in range(1, 13):
    if i == 12:
        width_rule = "width: 100%;"
    else:
        width_rule = f"width: calc(((100% - 11 * var(--grid-gap)) / 12) * {i} + {i - 1} * var(--grid-gap));"

    stylesheet.add_class(f"col-{i}", style=width_rule)

stylesheet.add_raw(
    """
* { box-sizing: border-box; }

html { font-size: 16px; }

body {
  margin: 0;
  font-family: var(--font-sans);
  color: var(--color-text);
    background: radial-gradient(circle at 18% 14%, #231318, #0e0f14 68%);
  line-height: 1.5;
}

h1, h2, h3, h4, h5, h6 {
  margin: 0;
  line-height: 1.2;
  letter-spacing: -0.02em;
}

h1 { font-size: clamp(2rem, 4vw, 3rem); }
h2 { font-size: clamp(1.5rem, 2.5vw, 2rem); }

p { margin: 0; color: var(--color-text-soft); }

a { color: var(--color-primary); text-decoration: none; }
a:hover { text-decoration: underline; }

img, svg, video { max-width: 100%; display: block; }

button, input, select, textarea { font: inherit; }

:focus-visible { outline: none; box-shadow: var(--shadow-focus); }

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(14px); }
  to { opacity: 1; transform: translateY(0); }
}
"""
)

stylesheet.add_class("section", Style(padding_block="var(--space-10)"))

stylesheet.add_class(
    "surface",
    Style(
        background="var(--color-surface)",
        border="1px solid var(--color-border)",
        border_radius="var(--radius-xl)",
        box_shadow="var(--shadow-soft)",
        padding="2rem"
    ),
)

stylesheet.add_class("mono", Style(font_family="var(--font-mono)"))

stylesheet.add_class("fade-up", Style(animation="fadeUp 520ms ease both"))

stylesheet.add_class("delay-1", Style(animation_delay="80ms"))
stylesheet.add_class("delay-2", Style(animation_delay="160ms"))
stylesheet.add_class("delay-3", Style(animation_delay="240ms"))

# Use raw CSS for combinator selectors.
stylesheet.add_raw(
    """
.stack-sm > * + * { margin-top: var(--space-2); }
.stack-md > * + * { margin-top: var(--space-4); }
.stack-lg > * + * { margin-top: var(--space-6); }
"""
)

stylesheet.add_class(
    "container",
    Style(
        width="100%",
        margin_inline="auto",
        padding_inline="var(--space-4)",
        max_width="var(--container-xl)",
    ),
)

stylesheet.add_class(
    "container-fluid",
    Style(width="100%", margin_inline="auto", padding_inline="var(--space-4)"),
)

stylesheet.add_class(
    "row", Style(display=Display.FLEX, flex_wrap="wrap", gap="1rem")
)

stylesheet.add_class(
    "grid",
    Style(
        display=Display.GRID,
        gap="var(--space-4)",
    ),
)

stylesheet.add_class("grid-2", Style(grid_template_columns="repeat(2, minmax(0, 1fr))"))

stylesheet.add_class("grid-3", Style(grid_template_columns="repeat(3, minmax(0, 1fr))"))

stylesheet.add_class("grid-4", Style(grid_template_columns="repeat(4, minmax(0, 1fr))"))

stylesheet.add_class("d-flex", Style(display=Display.FLEX))

stylesheet.add_class("flex-row", Style(flex_direction="row"))

stylesheet.add_class("flex-column", Style(flex_direction="column"))

stylesheet.add_class("flex-wrap", Style(flex_wrap="wrap"))

stylesheet.add_class("justify-start", Style(justify_content="flex-start"))

stylesheet.add_class("justify-center", Style(justify_content="center"))

stylesheet.add_class("justify-end", Style(justify_content="flex-end"))

stylesheet.add_class("justify-between", Style(justify_content="space-between"))

stylesheet.add_class("item-start", Style(align_items="flex-start"))

stylesheet.add_class("item-center", Style(align_items="center"))

stylesheet.add_class("item-end", Style(align_items="flex-end"))

stylesheet.add_class("gap-2", Style(gap="var(--space-2)"))

stylesheet.add_class("gap-4", Style(gap="var(--space-4)"))

stylesheet.add_class("gap-6", Style(gap="var(--space-6)"))

stylesheet.add_class("grow-1", Style(flex="1 1 auto"))

stylesheet.add_raw(
    """
@media (min-width: 768px) {
	.container {
		max-width: var(--container-md);
	}

	.col-md-1 { width: calc((100% - 11 * var(--grid-gap)) / 12); }
	.col-md-2 { width: calc(((100% - 11 * var(--grid-gap)) / 12) * 2 + var(--grid-gap)); }
	.col-md-3 { width: calc(((100% - 11 * var(--grid-gap)) / 12) * 3 + 2 * var(--grid-gap)); }
	.col-md-4 { width: calc(((100% - 11 * var(--grid-gap)) / 12) * 4 + 3 * var(--grid-gap)); }
	.col-md-5 { width: calc(((100% - 11 * var(--grid-gap)) / 12) * 5 + 4 * var(--grid-gap)); }
	.col-md-6 { width: calc(((100% - 11 * var(--grid-gap)) / 12) * 6 + 5 * var(--grid-gap)); }
	.col-md-7 { width: calc(((100% - 11 * var(--grid-gap)) / 12) * 7 + 6 * var(--grid-gap)); }
	.col-md-8 { width: calc(((100% - 11 * var(--grid-gap)) / 12) * 8 + 7 * var(--grid-gap)); }
	.col-md-9 { width: calc(((100% - 11 * var(--grid-gap)) / 12) * 9 + 8 * var(--grid-gap)); }
	.col-md-10 { width: calc(((100% - 11 * var(--grid-gap)) / 12) * 10 + 9 * var(--grid-gap)); }
	.col-md-11 { width: calc(((100% - 11 * var(--grid-gap)) / 12) * 11 + 10 * var(--grid-gap)); }
	.col-md-12 { width: 100%; }
}

@media (min-width: 1024px) {
	.container {
		max-width: var(--container-lg);
	}

	.col-lg-1 { width: calc((100% - 11 * var(--grid-gap)) / 12); }
	.col-lg-2 { width: calc(((100% - 11 * var(--grid-gap)) / 12) * 2 + var(--grid-gap)); }
	.col-lg-3 { width: calc(((100% - 11 * var(--grid-gap)) / 12) * 3 + 2 * var(--grid-gap)); }
	.col-lg-4 { width: calc(((100% - 11 * var(--grid-gap)) / 12) * 4 + 3 * var(--grid-gap)); }
	.col-lg-5 { width: calc(((100% - 11 * var(--grid-gap)) / 12) * 5 + 4 * var(--grid-gap)); }
	.col-lg-6 { width: calc(((100% - 11 * var(--grid-gap)) / 12) * 6 + 5 * var(--grid-gap)); }
	.col-lg-7 { width: calc(((100% - 11 * var(--grid-gap)) / 12) * 7 + 6 * var(--grid-gap)); }
	.col-lg-8 { width: calc(((100% - 11 * var(--grid-gap)) / 12) * 8 + 7 * var(--grid-gap)); }
	.col-lg-9 { width: calc(((100% - 11 * var(--grid-gap)) / 12) * 9 + 8 * var(--grid-gap)); }
	.col-lg-10 { width: calc(((100% - 11 * var(--grid-gap)) / 12) * 10 + 9 * var(--grid-gap)); }
	.col-lg-11 { width: calc(((100% - 11 * var(--grid-gap)) / 12) * 11 + 10 * var(--grid-gap)); }
	.col-lg-12 { width: 100%; }
}
"""
)

# Badge

stylesheet.add_class("badge", Style(
    display=Display.INLINE_BLOCK,
    align_items=Align.CENTER,
    border_radius="var(--radius-pill)",
    font_weight=700,
    padding="0.25rem 0.65rem",
    font_size="0.75rem",
    letter_spacing="0.02em",
))

stylesheet.add_class("badge-neutral", Style(
    color="var(--color-text)",
    background="var(--color-surface-strong)",
))

stylesheet.add_class("badge-primary", Style(
    color="var(--color-primary)",
    background="rgba(139, 30, 45, 0.18)",
))

stylesheet.add_class("badge-success", Style(
    color="var(--color-success)",
    background="var(--color-success-soft)",
))

stylesheet.add_class("badge-danger", Style(
    color="var(--color-danger)",
    background="var(--color-danger-soft)",
))

# Card

stylesheet.add_class("card", Style(
    background="var(--color-surface)",
    border="1px solid var(--color-border)",
    border_radius="var(--radius-xl)",
    padding="var(--space-6)",
    box_shadow="var(--shadow-soft)"
))

stylesheet.add_class("card-header", Style(
    display=Display.FLEX,
    align_items=Align.CENTER,
    justify_content=Align.SPACE_BETWEEN,
    gap="var(--space-4)",
    margin_button="var(--space-4)"
))

stylesheet.add_class("card-title", Style(
    font_size="1.125rem"
))

stylesheet.add_class("card-subtitle", Style(
    color="var(--color-text-soft)",
    font_size="0.92rem",
))

stylesheet.add_class("card-content", Style(
    color="var(--color-text-soft)"
))

stylesheet.add_class("card-footer", Style(
    display=Display.FLEX,
    gap="var(--space-3)",
    margin_top="var(--space-5)"
))

# Buttons

stylesheet.add_class("btn", Style(
    display=Display.INLINE_FLEX,
    align_items=Align.CENTER,
    justify_content=Align.CENTER,
    gap="var(--space-2)",
    border="1px solid transparent",
    border_radius="var(--radius-md)",
    background="var(--color-surface)",
    color="var(--color-text)",
    padding="0.625rem 1rem",
    font_weight=600,
    line_height=1,
    cursor="pointer",
    box_shadow="var(--shadow-soft)",
    transition="transform var(--transition-fast), background-color var(--transition-fast), border-color var(--transition-fast)",
))

stylesheet.add_class("btn:hover", Style(
    transform="translateY(-1px)",
))

stylesheet.add_class("btn:active", Style(
    transform="translateY(0)",
    box_shadow="var(--shadow-soft-inset)",
))

stylesheet.add_class("btn-primary", Style(
    background="linear-gradient(145deg, var(--color-primary-strong), var(--color-primary))",
    border_color="var(--color-primary)",
    color="#fff",
))

stylesheet.add_class("btn-primary:hover", Style(
    background="linear-gradient(145deg, #c2364b, var(--color-primary-strong))"
))

stylesheet.add_class("btn-secondary", Style(
    background="var(--color-surface-strong)",
    border_color="var(--color-border)",
    color="var(--color-text)"
))

stylesheet.add_class("btn-ghost", Style(
    background="transparent",
    border_color="var(--color-border)",
    color="var(--color-primary)",
    box_shadow="none",
))

stylesheet.add_class("btn-danger", Style(
    background="linear-gradient(145deg, #dc5a5a, var(--color-danger))",
    border_color="var(--color-danger)",
    color="#fff",
))

stylesheet.add_class("btn-sm", Style(
    padding="0.45rem 0.75rem",
    font_size="0.875rem",
))

stylesheet.add_class("btn-lg", Style(
    padding="0.825rem 1.25rem",
    font_size="1.05rem",
))

stylesheet.add_class("btn-block", Style(
    width="100%",
))

disabled_style = Style(
    opacity="0.55",
    cursor="not-allowed",
    transform="none",
    box_shadow="none"
)

stylesheet.add_class("btn[disabled]", disabled_style)
stylesheet.add_class("btn.is-disabled", disabled_style)

stylesheet.add_class("btn.is-loading", Style(
    position="relative",
    color="transparent"
))

stylesheet.add_class("btn.is-loading::after", Style(
    content="\"\"",
    width="1em",
    height="1em",
    border_radius="var(--radius-pill)",
    border="2px solid rgba(255, 255, 255, 0.55)",
    border_top_color="#fff",
    position='absolute',
    animation="spin 900ms linear infinite"
))

stylesheet.add_raw(
"""
@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}
"""
)

# Alert

stylesheet.add_class("alert", Style(
    border="1px solid transparent",
    border_radius="var(--radius-lg)",
    padding="0.8rem 1rem",
    display=Display.GRID,
    gap="0.2rem",
))

stylesheet.add_class("alert-title", Style(
    font_weight=700,
    font_size="0.95rem",
))

stylesheet.add_raw(
"""
.alert p {
    font-size: 0.9rem;
}
"""
)

stylesheet.add_class("alert-info", Style(
    background="var(--color-info-soft)",
    border_color="var(--color-info)",
    color="var(--color-text)",
))

stylesheet.add_class("alert-success", Style(
    background="var(--color-success-soft)",
    border_color="var(--color-success)",
    color="var(--color-text)",
))

stylesheet.add_class("alert-warning", Style(
    background="var(--color-warning-soft)",
    border_color="var(--color-warning)",
    color="var(--color-text)",
))

stylesheet.add_class("alert-danger", Style(
    background="var(--color-danger-soft)",
    border_color="var(--color-danger)",
    color="var(--color-text)",
))

# Forms

stylesheet.add_class("form", Style(
    display=Display.GRID,
    gap="var(--space-5)",
))

stylesheet.add_class("form-group", Style(
    display=Display.GRID,
    gap="var(--space-2)",
))

stylesheet.add_class("label", Style(
    font_size="0.92rem",
    font_weight=700,
    color="var(--color-text)",
))

control_style = Style(
    width="100%",
    border="1px solid var(--color-border)",
    border_radius="var(--radius-md)",
    background="var(--color-surface-strong)",
    color="var(--color-text)",
    padding="0.65rem 0.85rem",
    transition="border-color var(--transition-fast), box-shadow var(--transition-fast)",
)

stylesheet.add_class("input", control_style)
stylesheet.add_class("select", control_style)
stylesheet.add_class("textarea", control_style)

stylesheet.add_class("textarea", Style(
    min_height="110px",
    resize="vertical",
))

stylesheet.add_class("input::placeholder", Style(color="#8a96a6"))
stylesheet.add_class("textarea::placeholder", Style(color="#8a96a6"))

stylesheet.add_class("input:focus", Style(border_color="var(--color-primary)"))
stylesheet.add_class("select:focus", Style(border_color="var(--color-primary)"))
stylesheet.add_class("textarea:focus", Style(border_color="var(--color-primary)"))

stylesheet.add_class("help-text", Style(
    font_size="0.82rem",
    color="var(--color-text-soft)",
))

stylesheet.add_raw(
"""
.is-invalid .input,
.is-invalid .select,
.is-invalid .textarea,
.input.is-invalid,
.select.is-invalid,
.textarea.is-invalid {
    border-color: var(--color-danger);
    background: rgba(209, 67, 67, 0.14);
}

.is-valid .input,
.is-valid .select,
.is-valid .textarea,
.input.is-valid,
.select.is-valid,
.textarea.is-valid {
    border-color: var(--color-success);
    background: rgba(47, 155, 101, 0.14);
}

.choice input {
    accent-color: var(--color-primary);
}
"""
)

stylesheet.add_class("error-text", Style(
    font_size="0.82rem",
    color="var(--color-danger)",
))

stylesheet.add_class("choice", Style(
    display=Display.INLINE_FLEX,
    align_items=Align.CENTER,
    gap="var(--space-2)",
    color="var(--color-text-soft)",
))

stylesheet.add_class("form-actions", Style(
    display=Display.FLEX,
    flex_wrap="wrap",
    gap="var(--space-3)",
))

