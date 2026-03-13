import astris
import pytest
from astris.stylesheet import StyleSheet
from astris.themes.bootstrap import theme as bootstrap_theme
from astris.themes.ember_dark import theme as ember_dark_theme
from astris.theme import Theme, create_default_theme, create_soft_theme


def test_theme_from_dict_and_to_css_variables() -> None:
    theme = Theme.from_dict(
        {
            "mode": "dark",
            "colors": {"bg": "#0f0f0f"},
            "spacing": {"md": "1rem"},
            "scales": {"radius": {"md": "8px"}},
            "components": {"button": {"class_name": "btn"}},
            "stylesheets": ["https://cdn.example.com/base.css", "/assets/site.css"],
            "extras": {"brand": "astris"},
        }
    )

    variables = theme.to_css_variables()

    assert theme.mode == "dark"
    assert variables["--color-bg"] == "#0f0f0f"
    assert variables["--space-md"] == "1rem"
    assert variables["--radius-md"] == "8px"
    assert theme.stylesheets == ["https://cdn.example.com/base.css", "/assets/site.css"]
    assert theme.extras["brand"] == "astris"


def test_theme_extend_merges_nested_mappings() -> None:
    base = Theme(
        mode="light",
        colors={"bg": "#ffffff", "fg": "#111111"},
        spacing={"sm": "0.5rem"},
        scales={"radius": {"sm": "4px"}},
        components={"div": {"class_name": "surface"}},
        stylesheets=["https://cdn.example.com/base.css"],
    )

    extended = base.extend(
        mode="dark",
        colors={"bg": "#000000"},
        scales={"radius": {"md": "8px"}},
        components={"div": {"data_variant": "elevated"}},
        stylesheets=["/assets/app.css", "https://cdn.example.com/base.css"],
    )

    assert base.mode == "light"
    assert extended.mode == "dark"
    assert extended.colors == {"bg": "#000000", "fg": "#111111"}
    assert extended.scales["radius"] == {"sm": "4px", "md": "8px"}
    assert extended.components["div"] == {
        "class_name": "surface",
        "data_variant": "elevated",
    }
    assert extended.stylesheets == [
        "https://cdn.example.com/base.css",
        "/assets/app.css",
    ]


def test_theme_stylesheets_are_normalized_and_deduplicated() -> None:
    theme = Theme(
        stylesheets=[
            "  https://cdn.example.com/base.css  ",
            "/assets/site.css",
            "https://cdn.example.com/base.css",
        ]
    )

    assert theme.stylesheets == ["https://cdn.example.com/base.css", "/assets/site.css"]


def test_theme_add_stylesheet_rejects_invalid_href() -> None:
    theme = Theme()

    theme.add_stylesheet("assets/site.css")
    assert theme.stylesheets == ["assets/site.css"]

    with pytest.raises(ValueError):
        theme.add_stylesheet("http://cdn.example.com/base.css")

    with pytest.raises(ValueError):
        theme.add_stylesheet("mailto:test@example.com")


def test_theme_can_attach_and_retrieve_stylesheet() -> None:
    theme = Theme()
    stylesheet = StyleSheet()

    theme.set_stylesheet(stylesheet)

    assert theme.get_stylesheet() is stylesheet


def test_theme_extend_keeps_stylesheet_by_default() -> None:
    stylesheet = StyleSheet()
    base = Theme(stylesheet=stylesheet)

    extended = base.extend(colors={"bg": "#000"})

    assert extended.get_stylesheet() is stylesheet


def test_theme_extend_allows_overriding_stylesheet() -> None:
    base = Theme(stylesheet=StyleSheet())
    custom = StyleSheet()

    extended = base.extend(stylesheet=custom)

    assert extended.get_stylesheet() is custom


def test_theme_component_defaults_merge_by_key_order() -> None:
    theme = Theme(
        components={
            "div": {"class_name": "surface", "id": "tag-id"},
            "Div": {"id": "class-id"},
        }
    )

    defaults = theme.component_defaults("div", "Div")

    assert defaults["class_name"] == "surface"
    assert defaults["id"] == "class-id"


def test_create_default_theme_light_includes_expected_tokens() -> None:
    theme = create_default_theme()

    assert theme.mode == "light"
    assert theme.extras["name"] == "astris-default"
    assert theme.colors["bg"] == "#ffffff"
    assert theme.spacing["md"] == "1rem"
    assert "radius" in theme.scales
    assert "body" in theme.components


def test_create_default_theme_dark_changes_palette() -> None:
    theme = create_default_theme("dark")

    assert theme.mode == "dark"
    assert theme.colors["bg"] == "#020617"
    assert theme.colors["fg"] == "#e2e8f0"


def test_default_theme_factory_is_exported() -> None:
    assert "create_default_theme" in astris.__all__


def test_create_soft_theme_light_overrides_default_tokens() -> None:
    theme = create_soft_theme("light")

    assert theme.mode == "light"
    assert theme.extras["name"] == "astris-soft"
    assert theme.extras["base"] == "astris-default"
    assert theme.colors["primary"] == "#8b5cf6"
    assert theme.spacing["sm"] == "0.625rem"
    assert "radius" in theme.scales


def test_create_soft_theme_dark_palette() -> None:
    theme = create_soft_theme("dark")

    assert theme.mode == "dark"
    assert theme.colors["bg"] == "#16141f"
    assert theme.colors["primary"] == "#c4b5fd"


def test_soft_theme_factory_is_exported() -> None:
    assert "create_soft_theme" in astris.__all__


def test_ember_dark_theme_uses_dark_mode_and_red_primary() -> None:
    assert ember_dark_theme.mode == "dark"
    assert ember_dark_theme.colors["bg"] == "#0e0f14"
    assert ember_dark_theme.colors["primary"] == "#8b1e2d"


def test_ember_dark_theme_has_attached_stylesheet() -> None:
    assert ember_dark_theme.get_stylesheet() is not None


def test_ember_dark_theme_metadata_name() -> None:
    assert ember_dark_theme.extras["name"] == "astris-ember-dark"


def test_bootstrap_theme_uses_light_mode_and_primary() -> None:
    assert bootstrap_theme.mode == "light"
    assert bootstrap_theme.colors["primary"] == "#0d6efd"


def test_bootstrap_theme_loads_bootstrap_cdn() -> None:
    assert bootstrap_theme.stylesheets == [
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
    ]


def test_bootstrap_theme_has_attached_stylesheet() -> None:
    assert bootstrap_theme.get_stylesheet() is not None
