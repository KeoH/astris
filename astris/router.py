from dataclasses import dataclass
from typing import Any, Callable, Mapping, Sequence

from .component import Component


@dataclass(frozen=True)
class PageRegistration:
    path: str
    factory: Callable[..., Component]
    static_params: Sequence[Mapping[str, Any]] | None = None


class Router:
    def __init__(self, prefix: str = ""):
        self.prefix = self._normalize_prefix(prefix)
        self._pages: list[PageRegistration] = []

    def _normalize_prefix(self, prefix: str) -> str:
        if not prefix:
            return ""

        normalized = prefix if prefix.startswith("/") else f"/{prefix}"
        if len(normalized) > 1:
            normalized = normalized.rstrip("/")
        return normalized

    def _join_path(self, path: str) -> str:
        if not path:
            raise ValueError("Route path cannot be empty")

        normalized = path if path.startswith("/") else f"/{path}"
        if len(normalized) > 1:
            normalized = normalized.rstrip("/")

        if not self.prefix:
            return normalized
        if normalized == "/":
            return self.prefix
        return f"{self.prefix}{normalized}"

    def page(
        self,
        path: str,
        static_params: Sequence[Mapping[str, Any]] | None = None,
    ):
        """Decorator to register a page on this router."""

        def decorator(func: Callable[..., Component]) -> Callable[..., Component]:
            full_path = self._join_path(path)
            self._pages.append(
                PageRegistration(
                    path=full_path,
                    factory=func,
                    static_params=static_params,
                )
            )
            return func

        return decorator

    def iter_pages(self) -> list[PageRegistration]:
        return list(self._pages)
