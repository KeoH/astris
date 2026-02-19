# Quickstart

## Create a new project

```bash
uvx astris new my-project
cd my-project
uv run python main.py
```

## Build static output

```bash
uv run astris build
```

## Minimal app example

```python
from astris import AstrisApp
from astris.lib import Body, H1, Html

app = AstrisApp()


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

## Add assets in the page head

```python
from astris import AstrisApp

app = AstrisApp()

app.add_head_link(
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
)
app.add_head_script(
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
)
```
