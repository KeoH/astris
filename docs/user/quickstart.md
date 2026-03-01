# Quickstart

## Create a new project

```bash
uvx astris new my-project
cd my-project
uv sync
uv run python main.py
```

The generated project uses `pyproject.toml` for dependencies and does not include `requirements.txt`.

## Build static output

```bash
uv run astris build
```

## Deploy to Cloudflare Pages

```bash
uv run astris deploy
```

For full setup (including Git-based deployment in Cloudflare), see `deployment.md`.

## Minimal app example

```python
from astris import Astris
from astris.lib import Body, H1, Html

app = Astris()


@app.page("/")
def home():
    return Html(children=[
        Body(children=[
            H1(children=["Hello from Astris"]),
        ])
    ])


if __name__ == "__main__":
    app.run_dev()
```

## Configure a theme

Use a built-in preset:

```python
from astris import Astris, create_default_theme

app = Astris(theme=create_default_theme("dark"))
```

You can also use:

```python
from astris import Astris, create_soft_theme

app = Astris(theme=create_soft_theme("light"))
```

For full configuration, component defaults, and runtime switching, see [Themes](themes.md).
That guide also covers responsive design with `add_media_query(...)`.

## Add assets in the page head

```python
from astris import Astris

app = Astris()

app.add_head_link(
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
)
app.add_head_script(
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
)
```

## Available HTML wrappers

`astris.lib` includes wrappers for the modern standard HTML tags (A to Z).
All wrapper classes include short English docstrings, and void tags such as `Img`, `Br`, and `Input` render without closing tags.

Layout helpers are provided by `astris.layout`:

```python
from astris.layout import Container, Column, Row
```

## JSON content collections

You can register a directory of JSON files as read-only content and render detail pages from a Python template.

```python
from astris import Astris, Text, register_json_collection
from astris.lib import Body, Div, Html

app = Astris()


def post_template(entry: dict):
    return Html(children=[
        Body(children=[
            Div(children=[Text(entry["title"])]),
        ])
    ])


posts = register_json_collection(
    app,
    name="posts",
    directory="content/posts",
    template=post_template,
    api_prefix="/api/collections",
)

print(posts.page_links())
```

Behavior:

- Generates detail routes at `/<collection>/<slug>`.
- Exposes read-only dev endpoints:
  - `GET /api/collections/<collection>`
  - `GET /api/collections/<collection>/<slug>`
- Uses `slug` from JSON when present; otherwise it falls back to the file name.
