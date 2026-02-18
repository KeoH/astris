import os
import re
import sys
from pathlib import Path
from typing import Dict
from urllib.parse import urlsplit, urlunsplit

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from .component import Component


class AstrisApp:
    def __init__(self):
        self.routes: Dict[str, Component] = {}
        self._fastapi_app = FastAPI()

    def page(self, path: str):
        """Decorator to register a page (route)."""

        def decorator(func):
            component_tree = func()
            self.routes[path] = component_tree

            @self._fastapi_app.get(path, response_class=HTMLResponse)
            async def serve_page():
                return f"<!DOCTYPE html>{component_tree.render()}"

            return func

        return decorator

    def _infer_import_string(self) -> str | None:
        main_module = sys.modules.get("__main__")
        main_file = getattr(main_module, "__file__", None)
        if not main_file:
            return None

        module_name = Path(main_file).stem
        return f"{module_name}:app._fastapi_app"

    def run_dev(self, port=8000, reload=True):
        """Start the development server."""
        print(f"🚀 Dev server running at http://localhost:{port}")

        if reload:
            import_string = self._infer_import_string()
            if import_string:
                uvicorn.run(
                    import_string,
                    host="0.0.0.0",
                    port=port,
                    reload=True,
                    reload_dirs=[os.getcwd()],
                )
                return

            print("⚠️ Could not infer the main module, starting without hot reload.")

        uvicorn.run(self._fastapi_app, host="0.0.0.0", port=port)

    def _route_to_filename(self, route: str) -> str:
        normalized = route if route.startswith("/") else f"/{route}"
        if normalized == "/":
            return "index.html"
        return f"{normalized.strip('/')}.html"

    def _resolve_route(self, path: str) -> str | None:
        if path in self.routes:
            return path

        without_slash = path.rstrip("/")
        if without_slash and without_slash in self.routes:
            return without_slash

        with_slash = f"{without_slash}/"
        if with_slash in self.routes:
            return with_slash

        return None

    def _rewrite_static_links(self, current_route: str, html: str) -> str:
        current_file = self._route_to_filename(current_route)
        current_dir = os.path.dirname(current_file) or "."

        def replace_href(match: re.Match[str]) -> str:
            quote = match.group("quote")
            href_value = match.group("href")

            split = urlsplit(href_value)
            if split.scheme or split.netloc or split.path.startswith("//"):
                return match.group(0)

            resolved_route = self._resolve_route(split.path)
            if not resolved_route:
                return match.group(0)

            target_file = self._route_to_filename(resolved_route)
            relative_target = os.path.relpath(target_file, start=current_dir).replace(
                os.sep, "/"
            )
            rebuilt_href = urlunsplit(
                ("", "", relative_target, split.query, split.fragment)
            )

            return f"href={quote}{rebuilt_href}{quote}"

        return re.sub(
            r'href=(?P<quote>["\'])(?P<href>.*?)(?P=quote)',
            replace_href,
            html,
        )

    def build(self, output_dir="dist"):
        """Generate static HTML files."""
        print(f"📦 Building site into ./{output_dir}...")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for path, component in self.routes.items():
            filename = self._route_to_filename(path)
            filepath = os.path.join(output_dir, filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            rendered_html = self._rewrite_static_links(path, component.render())

            with open(filepath, "w", encoding="utf-8") as f:
                f.write("<!DOCTYPE html>\n")
                f.write(rendered_html)

            print(f"  ✅ Generated: {filepath}")

        print("✨ Build completed successfully.")
