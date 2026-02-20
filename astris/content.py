import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, List, Sequence

from .component import Component

TemplateFactory = Callable[[Any], Component]


@dataclass(frozen=True)
class JsonCollectionEntry:
    slug: str
    route: str
    data: Any
    source: str


@dataclass(frozen=True)
class JsonCollection:
    name: str
    route_prefix: str
    api_prefix: str
    entries: Sequence[JsonCollectionEntry]

    def page_links(self) -> List[str]:
        return [entry.route for entry in self.entries]

    def to_api_payload(self) -> List[dict[str, Any]]:
        return [
            {
                "slug": entry.slug,
                "route": entry.route,
                "source": entry.source,
                "data": entry.data,
            }
            for entry in self.entries
        ]


def _slugify(value: str) -> str:
    candidate = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return candidate or "item"


def _normalize_prefix(prefix: str) -> str:
    if not prefix:
        raise ValueError("Prefix cannot be empty")

    normalized = prefix if prefix.startswith("/") else f"/{prefix}"
    if len(normalized) > 1:
        normalized = normalized.rstrip("/")
    return normalized


def _load_collection_entries(
    directory: str | Path,
    slug_field: str,
    route_prefix: str,
) -> List[JsonCollectionEntry]:
    source_dir = Path(directory)
    if not source_dir.exists():
        raise FileNotFoundError(f"Collection directory does not exist: {source_dir}")
    if not source_dir.is_dir():
        raise ValueError(f"Collection path must be a directory: {source_dir}")

    entries: List[JsonCollectionEntry] = []
    seen_slugs: set[str] = set()

    for json_file in sorted(source_dir.glob("*.json")):
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        slug_value: str | None = None
        if isinstance(data, dict):
            value = data.get(slug_field)
            if isinstance(value, str) and value.strip():
                slug_value = value

        slug = _slugify(slug_value or json_file.stem)
        if slug in seen_slugs:
            raise ValueError(f"Duplicate slug '{slug}' in collection directory: {source_dir}")
        seen_slugs.add(slug)

        route = f"{route_prefix}/{slug}"
        entries.append(
            JsonCollectionEntry(
                slug=slug,
                route=route,
                data=data,
                source=str(json_file.name),
            )
        )

    return entries


def register_json_collection(
    app: Any,
    *,
    name: str,
    directory: str | Path,
    template: TemplateFactory,
    api_prefix: str = "/api/collections",
    route_prefix: str | None = None,
    slug_field: str = "slug",
) -> JsonCollection:
    if not name.strip():
        raise ValueError("Collection name cannot be empty")

    normalized_name = name.strip()
    normalized_route_prefix = _normalize_prefix(route_prefix or f"/{normalized_name}")
    normalized_api_prefix = _normalize_prefix(api_prefix)

    entries = _load_collection_entries(directory, slug_field, normalized_route_prefix)

    for entry in entries:
        component = template(entry.data)
        if not isinstance(component, Component):
            raise TypeError("Collection template must return an Astris Component")
        app._register_component_route(entry.route, component)

    collection = JsonCollection(
        name=normalized_name,
        route_prefix=normalized_route_prefix,
        api_prefix=normalized_api_prefix,
        entries=entries,
    )
    app._register_collection_api(
        collection_name=normalized_name,
        entries=collection.to_api_payload(),
        api_prefix=normalized_api_prefix,
    )
    return collection
