# Theme Creation Checklist

## Structure

- Create `astris/themes/<theme_name>/`.
- Add `__init__.py` exporting `theme`.
- Add `stylesheet.py` with shared classes.
- Add optional `components.py` for wrappers.
- Add optional `layout.py` for page shell.

## Theme tokens

- Define semantic `colors` tokens.
- Define reusable `spacing` tokens.
- Define optional `scales` groups (shadow/radius/container/font/etc).
- Keep token naming consistent with `var(--color-*)`, `var(--space-*)`, and `var(--<scale>-*)`.

## Styling

- Prefer `StyleSheet.add_class(...)` for reusable classes.
- Use `add_raw(...)` only for advanced selectors/keyframes.
- Verify responsive behavior via breakpoints or media queries.

## Components

- Keep wrappers thin over `astris.lib` primitives.
- Ensure class names map to stylesheet classes.
- Keep constructor arguments explicit and easy to consume.

## Validation

- Run targeted tests for affected modules.
- Validate render output includes theme CSS variables.
- Validate render output includes class-based CSS when stylesheet is attached.
- Build docs if user-facing docs were modified.
