---
name: create-astris-theme
description: Creates new Astris themes by scaffolding theme modules, defining tokens and stylesheet classes, and validating integration with app rendering and static build.
---

# Create Astris Theme Skill

This skill standardizes how to create a new theme under the Astris theme system.

## When to use this skill

- A user asks to create a new reusable theme package.
- A user wants to extend the design language with custom tokens and classes.
- A user asks for a starter template for a new theme folder.

## Out of scope

- Refactoring unrelated framework modules.
- Replacing existing default theme semantics unless requested.
- Publishing external packages.

## Project-specific constraints

- Keep themes under `astris/themes/<theme_name>/`.
- Follow the package layout used by `astris/themes/default/`.
- Export a `theme` object from the theme package `__init__.py`.
- Keep implementation explicit and minimal.
- Keep docs, comments, and docstrings in English.

## Decision tree

1. Determine scope:
   - If user wants a full theme package, create `__init__.py`, `stylesheet.py`, `components.py`, and `layout.py`.
   - If user wants token-only changes, create/update only `__init__.py` and optional `stylesheet.py`.
2. Determine baseline:
   - If user wants a fresh style language, define all tokens manually.
   - If user wants compatibility with existing UX, start from `create_default_theme(...)` and extend.
3. Determine component layer:
   - If user needs reusable UI primitives, add themed component wrappers.
   - Otherwise keep only stylesheet utilities.

## Required execution steps

1. Inspect current theme conventions:
   - `astris/theme.py`
   - `astris/stylesheet.py`
   - `astris/themes/default/__init__.py`
   - `astris/themes/default/stylesheet.py`
   - `astris/themes/default/components.py`
   - `astris/themes/default/layout.py`
2. Create target folder structure under `astris/themes/<name>/`.
3. Implement `__init__.py`:
   - Instantiate and export `theme`.
   - Attach stylesheet when applicable.
   - Define `colors`, `spacing`, and `scales` tokens.
4. Implement `stylesheet.py`:
   - Add semantic classes for layout and shared UI patterns.
   - Add raw CSS only for selectors or rules not handled by `add_class(...)`.
5. Implement optional `components.py` wrappers:
   - Build thin wrappers over primitives from `astris.lib`.
   - Keep constructor APIs simple and explicit.
6. Implement optional `layout.py` helper:
   - Provide a reusable page shell (`Html`, `Head`, `Body`, metadata).
7. Integrate and validate:
   - Use `app = Astris(theme=theme)` in a sample route.
   - Ensure CSS variables and class CSS are injected in rendered HTML.

## Validation notes

- Run tests that cover changed behavior.
- Build docs if user-facing docs were updated.
- Prefer substring assertions for generated CSS instead of exact full blocks.
- Confirm external stylesheet URLs use accepted formats (`https://...`, `/...`, relative paths).

## Output expectations

When finishing the task, report:

- Files created/updated.
- Theme API choices (tokens, stylesheet, component wrappers).
- Validation commands and outcomes.
- Any follow-up suggestions for extending the theme.
