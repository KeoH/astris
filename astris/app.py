import os
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping, Sequence
from urllib.parse import urlsplit, urlunsplit

import uvicorn
from fastapi import HTTPException
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .component import Component
from .theme import Theme, activate_theme, create_default_theme, deactivate_theme


PathParams = Dict[str, str]
PageFactory = Callable[[PathParams], Component]


@dataclass(frozen=True)
class DynamicRoute:
    path_pattern: str
    parameter_names: tuple[str, ...]
    render: PageFactory
    static_params: List[PathParams]


class Astris:
    def __init__(self, theme: Theme | None = None):
        self.routes: Dict[str, Component] = {}
        self._dynamic_routes: Dict[str, DynamicRoute] = {}
        self._collection_entries: Dict[str, List[Dict[str, Any]]] = {}
        self._collection_api_prefixes: Dict[str, str] = {}
        self._head_links: List[Dict[str, str]] = []
        self._head_scripts: List[Dict[str, str]] = []
        self.theme: Theme = theme if theme is not None else create_default_theme()
        self._fastapi_app = FastAPI()
        self._ensure_assets_mount()

    def _ensure_assets_mount(self, assets_dir: str = "assets") -> None:
        assets_path = Path(assets_dir)
        if not assets_path.is_dir():
            return

        for route in self._fastapi_app.routes:
            if getattr(route, "path", None) == "/assets":
                return

        self._fastapi_app.mount(
            "/assets",
            StaticFiles(directory=str(assets_path)),
            name="assets",
        )

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
        if normalized_path in self._dynamic_routes:
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

    def _extract_path_parameter_names(self, path: str) -> tuple[str, ...]:
        matches = re.findall(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}", path)
        if len(matches) != len(set(matches)):
            raise ValueError(f"Duplicate path parameter names are not allowed: {path}")
        return tuple(matches)

    def _validate_static_params(
        self,
        path: str,
        parameter_names: tuple[str, ...],
        static_params: Sequence[Mapping[str, Any]] | None,
    ) -> List[PathParams]:
        if not static_params:
            return []

        validated: List[PathParams] = []
        expected = set(parameter_names)

        for index, param_set in enumerate(static_params):
            provided = set(param_set.keys())
            if provided != expected:
                raise ValueError(
                    "static_params entry keys must exactly match route parameters "
                    f"for {path}; expected {sorted(expected)} got {sorted(provided)} "
                    f"at index {index}"
                )

            normalized_params: PathParams = {}
            for name in parameter_names:
                value = str(param_set[name])
                if "/" in value:
                    raise ValueError(
                        f"Path parameter '{name}' cannot contain '/': {value}"
                    )
                normalized_params[name] = value

            validated.append(normalized_params)

        return validated

    def _materialize_dynamic_path(self, path_pattern: str, params: Mapping[str, str]) -> str:
        materialized = path_pattern
        for name, value in params.items():
            materialized = materialized.replace(f"{{{name}}}", value)
        return self._normalize_route_path(materialized)

    def _register_dynamic_route(
        self,
        path: str,
        parameter_names: tuple[str, ...],
        factory: Callable[..., Component],
        static_params: Sequence[Mapping[str, Any]] | None,
    ) -> str:
        normalized_path = self._normalize_route_path(path)
        if normalized_path in self.routes or normalized_path in self._dynamic_routes:
            raise ValueError(f"Route already registered: {normalized_path}")

        validated_static_params = self._validate_static_params(
            normalized_path,
            parameter_names,
            static_params,
        )

        def render(path_params: PathParams) -> Component:
            return factory(**path_params)

        dynamic_route = DynamicRoute(
            path_pattern=normalized_path,
            parameter_names=parameter_names,
            render=render,
            static_params=validated_static_params,
        )
        self._dynamic_routes[normalized_path] = dynamic_route

        def serve_page(**path_params: str):
            component_tree = dynamic_route.render(path_params)
            return f"<!DOCTYPE html>{self._render_page_html(component_tree)}"

        self._fastapi_app.add_api_route(
            normalized_path,
            serve_page,
            methods=["GET"],
            response_class=HTMLResponse,
        )

        return normalized_path

    def _register_page_callable(
        self,
        path: str,
        factory: Callable[..., Component],
        static_params: Sequence[Mapping[str, Any]] | None = None,
    ) -> str:
        parameter_names = self._extract_path_parameter_names(path)
        if parameter_names:
            return self._register_dynamic_route(
                path,
                parameter_names,
                factory,
                static_params,
            )

        component_tree = factory()
        if not isinstance(component_tree, Component):
            raise TypeError("Page function must return an Astris Component")
        return self._register_component_route(path, component_tree)

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

    def _iter_theme_stylesheet_links(self) -> List[Dict[str, str]]:
        if self.theme is None:
            return []
        return [{"rel": "stylesheet", "href": href} for href in self.theme.stylesheets]

    def _render_link_tags(
        self,
        parts: List[str],
        links: List[Dict[str, str]],
        seen_hrefs: set[str],
    ) -> None:
        for link_attrs in links:
            href = link_attrs.get("href")
            if href and href in seen_hrefs:
                continue

            if href:
                seen_hrefs.add(href)

            attrs = self._render_tag_attributes(link_attrs)
            parts.append(f"<link {attrs}>")

    def _render_head_assets(self) -> str:
        parts: List[str] = []
        seen_hrefs: set[str] = set()

        self._render_link_tags(parts, self._iter_theme_stylesheet_links(), seen_hrefs)

        if self.theme is not None:
            theme_css = self.theme.to_style_block()
            parts.append(
                f'<style data-astris-theme="{self.theme.mode}">{theme_css}</style>'
            )

            theme_stylesheet = self.theme.get_stylesheet()
            if theme_stylesheet is not None:
                stylesheet_css = theme_stylesheet.render_css()
                if stylesheet_css:
                    parts.append(
                        f'<style data-astris-theme-classes="{self.theme.mode}">{stylesheet_css}</style>'
                    )

        self._render_link_tags(parts, self._head_links, seen_hrefs)

        for script_attrs in self._head_scripts:
            attrs = self._render_tag_attributes(script_attrs)
            parts.append(f"<script {attrs}></script>")

        return "".join(parts)

    def _inject_theme_mode(self, html: str) -> str:
        if self.theme is None:
            return html

        html_open_match = re.search(r"<html([^>]*)>", html, re.IGNORECASE)
        if not html_open_match:
            return html

        html_attributes = html_open_match.group(1)
        if re.search(r"\sdata-theme\s*=", html_attributes, re.IGNORECASE):
            return html

        insert_at = html_open_match.end() - 1
        return f'{html[:insert_at]} data-theme="{self.theme.mode}"{html[insert_at:]}'

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
        token = activate_theme(self.theme)
        try:
            html = component.render()
        finally:
            deactivate_theme(token)

        html = self._inject_theme_mode(html)
        return self._inject_head_assets(html)

    def page(
        self,
        path: str,
        static_params: Sequence[Mapping[str, Any]] | None = None,
    ):
        """Decorator to register a page (route)."""

        def decorator(func):
            self._register_page_callable(path, func, static_params=static_params)

            return func

        return decorator

    def include_router(self, router: Any) -> None:
        """Register all routes from a Router-like object."""
        if not hasattr(router, "iter_pages"):
            raise TypeError("Router must expose an iter_pages() method")

        for route in router.iter_pages():
            self._register_page_callable(
                route.path,
                route.factory,
                static_params=route.static_params,
            )

    def _infer_import_string(self) -> str | None:
        main_module = sys.modules.get("__main__")
        main_file = getattr(main_module, "__file__", None)
        if not main_file:
            return None

        module_name = Path(main_file).stem
        return f"{module_name}:app._fastapi_app"

    def run_dev(self, port=8000, reload=True):
        """Start the development server."""
        self._ensure_assets_mount()
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

    def _resolve_route(
        self,
        path: str,
        available_routes: set[str] | None = None,
    ) -> str | None:
        if not path:
            return None

        normalized_path = self._normalize_route_path(path)
        route_keys = available_routes if available_routes is not None else set(self.routes)

        if normalized_path in route_keys:
            return normalized_path

        without_slash = normalized_path.rstrip("/")
        if without_slash and without_slash in route_keys:
            return without_slash

        with_slash = f"{without_slash}/"
        if with_slash in route_keys:
            return with_slash

        return None

    def _is_absolute_href(self, split) -> bool:
        """Check if href is absolute (external link)."""
        return bool(split.scheme or split.netloc or split.path.startswith("//"))

    def _rewrite_asset_href(self, split, current_dir: str, quote: str) -> str | None:
        """Rewrite relative asset paths. Returns None if not an asset path."""
        normalized_relative_path = split.path
        if normalized_relative_path.startswith("./"):
            normalized_relative_path = normalized_relative_path[2:]

        is_asset = (
            normalized_relative_path == "assets"
            or normalized_relative_path.startswith("assets/")
        )
        if not is_asset:
            return None

        relative_target = os.path.relpath(
            normalized_relative_path,
            start=current_dir,
        ).replace(os.sep, "/")
        rebuilt_href = urlunsplit(
            ("", "", relative_target, split.query, split.fragment)
        )
        return f"href={quote}{rebuilt_href}{quote}"

    def _rewrite_route_href(
        self,
        split,
        current_dir: str,
        clean_urls: bool,
        quote: str,
        available_routes: set[str] | None = None,
    ) -> str | None:
        """Rewrite absolute route paths. Returns None if route not found."""
        resolved_route = self._resolve_route(split.path, available_routes=available_routes)
        if not resolved_route:
            return None

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

    def _rewrite_static_links(
        self,
        current_route: str,
        html: str,
        clean_urls: bool = False,
        available_routes: set[str] | None = None,
    ) -> str:
        current_file = self._route_to_filename(current_route, clean_urls=clean_urls)
        current_dir = os.path.dirname(current_file) or "."

        def replace_href(match: re.Match[str]) -> str:
            quote = match.group("quote")
            href_value = match.group("href")
            split = urlsplit(href_value)

            if self._is_absolute_href(split):
                return match.group(0)

            if split.path and not split.path.startswith("/"):
                asset_result = self._rewrite_asset_href(split, current_dir, quote)
                if asset_result is not None:
                    return asset_result
                return match.group(0)

            route_result = self._rewrite_route_href(
                split,
                current_dir,
                clean_urls,
                quote,
                available_routes=available_routes,
            )
            return route_result if route_result is not None else match.group(0)

        return re.sub(
            r'href=(?P<quote>["\'])(?P<href>.*?)(?P=quote)',
            replace_href,
            html,
        )

    def _copy_assets_for_build(
        self, output_dir: str, assets_dir: str = "assets"
    ) -> None:
        assets_path = Path(assets_dir)
        if not assets_path.is_dir():
            return

        destination = Path(output_dir) / "assets"
        shutil.copytree(assets_path, destination, dirs_exist_ok=True)
        print(f"  ✅ Copied assets: {destination}")

    def build(self, output_dir="dist", clean_urls: bool = False):
        """Generate static HTML files."""
        print(f"📦 Building site into ./{output_dir}...")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        build_routes: Dict[str, Component] = dict(self.routes)

        for route in self._dynamic_routes.values():
            if not route.static_params:
                raise ValueError(
                    "Dynamic route requires static_params for build: "
                    f"{route.path_pattern}"
                )

            for params in route.static_params:
                concrete_path = self._materialize_dynamic_path(route.path_pattern, params)
                if concrete_path in build_routes:
                    raise ValueError(
                        f"Build route already generated: {concrete_path}"
                    )
                component = route.render(dict(params))
                if not isinstance(component, Component):
                    raise TypeError("Page function must return an Astris Component")
                build_routes[concrete_path] = component

        available_routes = set(build_routes)

        for path, component in build_routes.items():
            filename = self._route_to_filename(path, clean_urls=clean_urls)
            filepath = os.path.join(output_dir, filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            rendered_html = self._rewrite_static_links(
                path,
                self._render_page_html(component),
                clean_urls=clean_urls,
                available_routes=available_routes,
            )

            with open(filepath, "w", encoding="utf-8") as f:
                f.write("<!DOCTYPE html>\n")
                f.write(rendered_html)

            print(f"  ✅ Generated: {filepath}")

        self._copy_assets_for_build(output_dir)

        print("✨ Build completed successfully.")
