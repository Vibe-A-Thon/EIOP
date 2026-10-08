"""Theme packages: brand tokens and per-tenant theme resolution (SR-WL-001).

A theme package bundles every visual identity token a white-label tenant
needs — logos, favicon, app name, colors, typography, spacing, icon set,
per-ontology node/edge visual styles, and light/dark variants — so a tenant
can be re-skinned without any code change.

``ThemeRegistry`` resolves the active theme for a tenant (explicit tenant
theme → platform default fallback). Persona styling for the AI assistant
(name/tone/avatar/greeting, SR-WL-003) rides on the same package; safety
behavior is not configurable here by design.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

_HEX_COLOR_RE = __import__("re").compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")


class ThemeMode(str, Enum):
    LIGHT = "light"
    DARK = "dark"


class LogoRef(BaseModel):
    """Reference to a tenant logo asset (storage key + optional href)."""

    model_config = ConfigDict(extra="forbid")

    key: str = Field(min_length=1, description="Object-storage key or URI of the asset")
    href: str | None = Field(default=None, description="Optional external URL override")
    alt: str = ""


class ColorPalette(BaseModel):
    """Semantic color tokens; values must be CSS hex colors."""

    model_config = ConfigDict(extra="forbid")

    primary: str
    secondary: str | None = None
    accent: str | None = None
    background: str | None = None
    surface: str | None = None
    text: str | None = None
    danger: str | None = None
    warning: str | None = None
    success: str | None = None

    @field_validator("*", mode="before")
    @classmethod
    def _hex(cls, value: Any) -> Any:
        if value is None:
            return value
        if isinstance(value, str) and _HEX_COLOR_RE.match(value):
            return value
        raise ValueError("color must be a hex string like '#1a2b3c'")


class Typography(BaseModel):
    model_config = ConfigDict(extra="forbid")

    font_family: str = Field(default="system-ui, sans-serif")
    mono_family: str | None = None
    base_size_px: int = Field(default=16, ge=10, le=32)
    scale_ratio: float = Field(default=1.25, ge=1.0, le=2.0)


class Spacing(BaseModel):
    model_config = ConfigDict(extra="forbid")

    unit_px: int = Field(default=4, ge=1, le=32)
    density: str = Field(default="comfortable", pattern="^(compact|comfortable|spacious)$")


class NodeStyle(BaseModel):
    """Visual style for one ontology vertex type (SR-WL-001 node/edge styles)."""

    model_config = ConfigDict(extra="forbid")

    ontology_type: str = Field(min_length=1, description="Canonical ontology type, e.g. 'Service'")
    color: str | None = None
    icon: str | None = None
    shape: str = Field(default="circle", pattern="^(circle|square|diamond|hexagon|pill)$")

    @field_validator("color", mode="before")
    @classmethod
    def _check_color(cls, value: Any) -> Any:
        if value is None:
            return value
        if isinstance(value, str) and _HEX_COLOR_RE.match(value):
            return value
        raise ValueError("color must be a hex string like '#1a2b3c'")


class EdgeStyle(BaseModel):
    """Visual style for one ontology edge type."""

    model_config = ConfigDict(extra="forbid")

    relationship_type: str = Field(min_length=1)
    color: str | None = None
    line_style: str = Field(default="solid", pattern="^(solid|dashed|dotted)$")
    width_px: int = Field(default=1, ge=1, le=12)

    @field_validator("color", mode="before")
    @classmethod
    def _check_color(cls, value: Any) -> Any:
        if value is None:
            return value
        if isinstance(value, str) and _HEX_COLOR_RE.match(value):
            return value
        raise ValueError("color must be a hex string like '#1a2b3c'")


class ThemeVariant(BaseModel):
    """Tokens for one mode (light or dark)."""

    model_config = ConfigDict(extra="forbid")

    mode: ThemeMode
    colors: ColorPalette
    background_image_key: str | None = None


class AssistantPersona(BaseModel):
    """White-label persona for the AI assistant (SR-WL-003).

    Presentation only — safety behavior and system instructions are not
    part of this model and cannot be overridden per tenant.
    """

    model_config = ConfigDict(extra="forbid")

    name: str = Field(default="Assistant", min_length=1, max_length=64)
    tone: str = Field(default="professional", pattern="^(professional|friendly|concise|playful)$")
    avatar_key: str | None = None
    greeting: str = ""


class ThemePackage(BaseModel):
    """A complete tenant theme package (SR-WL-001)."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(description="URN, e.g. urn:eoip:branding:theme:<slug>")
    name: str = Field(min_length=1, max_length=128)
    version: str = Field(default="1.0.0")
    app_name: str = Field(min_length=1, max_length=128)
    logos: dict[ThemeMode, LogoRef] = Field(default_factory=dict)
    favicon_key: str | None = None
    typography: Typography = Field(default_factory=Typography)
    spacing: Spacing = Field(default_factory=Spacing)
    icon_set: str = Field(default="default", pattern=r"^[a-z0-9][a-z0-9_-]*$")
    variants: dict[ThemeMode, ThemeVariant] = Field(
        default_factory=lambda: {ThemeMode.LIGHT: ThemeVariant(mode=ThemeMode.LIGHT, colors=ColorPalette(primary="#1a2b3c"))}
    )
    node_styles: dict[str, NodeStyle] = Field(default_factory=dict)
    edge_styles: dict[str, EdgeStyle] = Field(default_factory=dict)
    assistant: AssistantPersona = Field(default_factory=AssistantPersona)

    @field_validator("id")
    @classmethod
    def _urn(cls, value: str) -> str:
        if not value.startswith("urn:eoip:branding:theme:"):
            raise ValueError("theme id must be urn:eoip:branding:theme:<slug>")
        return value

    @model_validator(mode="after")
    def _light_variant_present(self) -> ThemePackage:
        if ThemeMode.LIGHT not in self.variants:
            raise ValueError("a light variant is required")
        return self

    def variant(self, mode: ThemeMode) -> ThemeVariant:
        """Resolve a variant, falling back from dark to light."""
        return self.variants.get(mode) or self.variants[ThemeMode.LIGHT]

    def node_style(self, ontology_type: str) -> NodeStyle | None:
        return self.node_styles.get(ontology_type)


class ThemeRegistry:
    """Resolves the active theme package for a tenant (SR-WL-001).

    Lookup order: tenant-specific theme id → platform default theme.
    """

    def __init__(self, default_theme: ThemePackage | None = None):
        self._themes: dict[str, ThemePackage] = {}
        self._tenant_theme: dict[str, str] = {}
        self._default_id: str | None = None
        if default_theme is not None:
            self.register(default_theme, default=True)

    def register(self, theme: ThemePackage, *, default: bool = False) -> None:
        self._themes[theme.id] = theme
        if default or self._default_id is None:
            self._default_id = theme.id

    def assign(self, tenant_id: str, theme_id: str) -> None:
        if theme_id not in self._themes:
            raise KeyError(f"unknown theme {theme_id}")
        self._tenant_theme[tenant_id] = theme_id

    def resolve(self, tenant_id: str | None = None, mode: ThemeMode = ThemeMode.LIGHT) -> ThemePackage:
        """Resolve the effective theme for a tenant (or the platform default)."""
        theme_id = self._tenant_theme.get(tenant_id or "") or self._default_id
        if theme_id is None:
            raise KeyError("no theme registered")
        return self._themes[theme_id]

    def resolve_view(self, tenant_id: str | None = None, mode: ThemeMode = ThemeMode.LIGHT) -> dict:
        """Resolved, client-ready token view (variant merged, mode applied)."""
        theme = self.resolve(tenant_id, mode)
        variant = theme.variant(mode)
        return {
            "theme_id": theme.id,
            "app_name": theme.app_name,
            "mode": variant.mode.value,
            "colors": variant.colors.model_dump(exclude_none=True),
            "typography": theme.typography.model_dump(),
            "spacing": theme.spacing.model_dump(),
            "icon_set": theme.icon_set,
            "logos": {k.value: v.model_dump(exclude_none=True) for k, v in theme.logos.items()},
            "node_styles": {k: v.model_dump(exclude_none=True) for k, v in theme.node_styles.items()},
            "edge_styles": {k: v.model_dump(exclude_none=True) for k, v in theme.edge_styles.items()},
            "assistant": theme.assistant.model_dump(exclude_none=True),
        }
