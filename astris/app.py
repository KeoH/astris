import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List
from urllib.parse import urlsplit, urlunsplit

import uvicorn
from fastapi import HTTPException
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse

from .component import Component


class Astris:
    def __init__(self):
        self.routes: Dict[str, Component] = {}
        self._collection_entries: Dict[str, List[Dict[str, Any]]] = {}
        self._collection_api_prefixes: Dict[str, str] = {}
        self._head_links: List[Dict[str, str]] = []
        self._head_scripts: List[Dict[str, str]] = []
        self._fastapi_app = FastAPI()

    def _normalize_route_path(self, path: str) -> str:
        if not path:
            raise ValueError("Route path cannot be empty")

        normalized = path if path.startswith("/") else f"/{path}"
        if len(normalized) > 1:
            normalized = normalized.rstrip("/")
        return normalized

    def _register_component_route(self, path: str, component: Component) -> str:
        normalized_path = self._normalize_route_path(path)
        if normalized_path in self.routes:
            raise ValueError(f"Route already registered: {normalized_path}")

        self.routes[normalized_path] = component
        component_tree = component

        def serve_page():
            return f"<!DOCTYPE html>{self._render_page_html(component_tree)}"

        self._fastapi_app.add_api_route(
            normalized_path,
            serve_page,
            methods=["GET"],
            response_class=HTMLResponse,
        )

        return normalized_path

    def _register_collection_api(
        self,
        collection_name: str,
        entries: List[Dict[str, Any]],
        api_prefix: str,
    ) -> None:
        normalized_prefix = self._normalize_route_path(api_prefix)

        if collection_name in self._collection_api_prefixes:
            previous = self._collection_api_prefixes[collection_name]
            if previous != normalized_prefix:
                raise ValueError(
                    "Collection already registered with a different API prefix: "
                    f"{collection_name}"
                )
            raise ValueError(f"Collection already registered: {collection_name}")

        self._collection_entries[collection_name] = entries
        self._collection_api_prefixes[collection_name] = normalized_prefix

        base_path = f"{normalized_prefix}/{collection_name}"
        collection_entries = self._collection_entries[collection_name]

        def list_entries():
            return JSONResponse(content=collection_entries)

        def get_entry(slug: str):
            for item in collection_entries:
                if item.get("slug") == slug:
                    return JSONResponse(content=item)
            raise HTTPException(status_code=404, detail="Collection entry not found")

        self._fastapi_app.add_api_route(
            base_path,
            list_entries,
            methods=["GET"],
            response_class=JSONResponse,
        )
        self._fastapi_app.add_api_route(
            f"{base_path}/{{slug}}",
            get_entry,
            methods=["GET"],
            response_class=JSONResponse,
        )

    def add_head_link(self, href: str, rel: str = "stylesheet", **attributes) -> None:
        """Register a link tag to be injected in the document head."""
        link_attrs = {"rel": rel, "href": href, **attributes}
        self._head_links.append({key: str(value) for key, value in link_attrs.items()})

    def add_head_script(self, src: str, **attributes) -> None:
        """Register a script tag to be injected in the document head."""
        script_attrs = {"src": src, **attributes}
        self._head_scripts.append(
            {key: str(value) for key, value in script_attrs.items()}
        )

    def _render_tag_attributes(self, attributes: Dict[str, str]) -> str:
        return " ".join([f'{key}="{value}"' for key, value in attributes.items()])

    def _render_head_assets(self) -> str:
        parts: List[str] = []
        for link_attrs in self._head_links:
            attrs = self._render_tag_attributes(link_attrs)
            parts.append(f"<link {attrs}>")

        for script_attrs in self._head_scripts:
            attrs = self._render_tag_attributes(script_attrs)
            parts.append(f"<script {attrs}></script>")

        return "".join(parts)

    def _inject_head_assets(self, html: str) -> str:
        head_assets = self._render_head_assets()
        if not head_assets:
            return html

        head_close_match = re.search(r"</head>", html, re.IGNORECASE)
        if head_close_match:
            insert_at = head_close_match.start()
            return f"{html[:insert_at]}{head_assets}{html[insert_at:]}"

        html_open_match = re.search(r"<html[^>]*>", html, re.IGNORECASE)
        if html_open_match:
            insert_at = html_open_match.end()
            return f"{html[:insert_at]}<head>{head_assets}</head>{html[insert_at:]}"

        return f"<head>{head_assets}</head>{html}"

    def _render_page_html(self, component: Component) -> str:
        return self._inject_head_assets(component.render())

    def page(self, path: str):
        """Decorator to register a page (route)."""

        def decorator(func):
            component_tree = func()
            self._register_component_route(path, component_tree)

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

    def _route_to_filename(self, route: str, clean_urls: bool = False) -> str:
        normalized = self._normalize_route_path(route)
        if normalized == "/":
            return "index.html"
        if clean_urls:
            return f"{normalized.strip('/')}/index.html"
        return f"{normalized.strip('/')}.html"

    def _resolve_route(self, path: str) -> str | None:
        if not path:
            return None

        normalized_path = self._normalize_route_path(path)

        if normalized_path in self.routes:
            return normalized_path

        without_slash = normalized_path.rstrip("/")
        if without_slash and without_slash in self.routes:
            return without_slash

        with_slash = f"{without_slash}/"
        if with_slash in self.routes:
            return with_slash

        return None

    def _rewrite_static_links(
        self, current_route: str, html: str, clean_urls: bool = False
    ) -> str:
        current_file = self._route_to_filename(current_route, clean_urls=clean_urls)
        current_dir = os.path.dirname(current_file) or "."

        def replace_href(match: re.Match[str]) -> str:
            quote = match.group("quote")
            href_value = match.group("href")

            split = urlsplit(href_value)
            if split.scheme or split.netloc or split.path.startswith("//"):
                return match.group(0)

            if split.path and not split.path.startswith("/"):
                return match.group(0)

            resolved_route = self._resolve_route(split.path)
            if not resolved_route:
                return match.group(0)

            if clean_urls:
                target_path = "/" if resolved_route == "/" else resolved_route
                rebuilt_href = urlunsplit(
                    ("", "", target_path, split.query, split.fragment)
                )
            else:
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

    def build(self, output_dir="dist", clean_urls: bool = False):
        """Generate static HTML files."""
        print(f"📦 Building site into ./{output_dir}...")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for path, component in self.routes.items():
            filename = self._route_to_filename(path, clean_urls=clean_urls)
            filepath = os.path.join(output_dir, filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            rendered_html = self._rewrite_static_links(
                path,
                self._render_page_html(component),
                clean_urls=clean_urls,
            )

            with open(filepath, "w", encoding="utf-8") as f:
                f.write("<!DOCTYPE html>\n")
                f.write(rendered_html)

            print(f"  ✅ Generated: {filepath}")

        print("✨ Build completed successfully.")
