from .app import Astris
from .component import Component, Element, Text
from .content import JsonCollection, JsonCollectionEntry, register_json_collection
from .core import AstrisApp
from .theme import Theme, create_default_theme, create_soft_theme

__version__ = "0.1.5"

__all__ = [
    "Astris",
    "AstrisApp",
    "Component",
    "Element",
    "Text",
    "JsonCollection",
    "JsonCollectionEntry",
    "register_json_collection",
    "Theme",
    "create_default_theme",
    "create_soft_theme",
    "__version__",
]
