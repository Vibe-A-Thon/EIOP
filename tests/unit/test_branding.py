"""Unit tests for white-label branding (SR-WL-001/003/006/007, SR-WL-004, SR-ONT-007)."""

from __future__ import annotations

import pytest
from eoip.branding import (
    ColorPalette,
    DeVendoringChecklist,
    IdentifierClass,
    IdentifierOverride,
    LegalContentKind,
    LegalContentRecord,
    LegalContentRegistry,
    LocalizationPack,
    LocalizationRegistry,
    NodeStyle,
    PoweredByToggle,
    TerminologyMap,
    TerminologyRegistry,
    ThemeMode,
    ThemePackage,
    ThemeRegistry,
    ThemeVariant,
)
from eoip.branding.router import build_router
from pydantic import ValidationError


def _theme(**over):
    base = {
        "id": "urn:eoip:branding:theme:default",
        "name": "Default",
        "app_name": "EOIP",
        "variants": {
            ThemeMode.LIGHT: ThemeVariant(mode=ThemeMode.LIGHT, colors=ColorPalette(primary="#112233")),
            ThemeMode.DARK: ThemeVariant(mode=ThemeMode.DARK, colors=ColorPalette(primary="#ddeeff")),
        },
    }
    base.update(over)
    return ThemePackage(**base)


# ---------------------------------------------------------------- theme ---

def test_theme_requires_urn_id():
    with pytest.raises(ValidationError):
        _theme(id="theme-1")


def test_theme_requires_light_variant():
    with pytest.raises(ValidationError):
        _theme(variants={ThemeMode.DARK: ThemeVariant(mode=ThemeMode.DARK, colors=ColorPalette(primary="#000000"))})


def test_theme_color_validation():
    with pytest.raises(ValidationError):
        ColorPalette(primary="not-a-color")
    with pytest.raises(ValidationError):
        NodeStyle(ontology_type="Service", color="red")


def test_theme_variant_dark_fallback():
    theme = _theme()
    assert theme.variant(ThemeMode.DARK).mode == ThemeMode.DARK


def test_registry_resolves_per_tenant():
    default = _theme()
    acme = _theme(id="urn:eoip:branding:theme:acme", app_name="AcmeLens")
    registry = ThemeRegistry(default_theme=default)
    registry.register(acme)
    assert registry.resolve("t-1").id == default.id
    registry.assign("t-acme", acme.id)
    assert registry.resolve("t-acme").app_name == "AcmeLens"
    view = registry.resolve_view("t-acme", ThemeMode.DARK)
    assert view["app_name"] == "AcmeLens"
    assert view["mode"] == "dark"
    with pytest.raises(KeyError):
        registry.assign("t-acme", "urn:eoip:branding:theme:missing")


# ---------------------------------------------------------- terminology ---

def test_terminology_round_trip():
    term = TerminologyMap(
        id="urn:eoip:branding:terminology:t-acme",
        tenant_id="t-acme",
        renames={"Service": "Application", "Incident": "Case"},
    )
    assert term.rename("Service") == "Application"
    assert term.rename("Deployment") == "Deployment"  # unchanged
    assert term.canonicalize("application") == "Service"
    assert term.canonicalize("Case") == "Incident"
    assert term.canonicalize("Unknown") == "Unknown"


def test_terminology_rejects_duplicate_labels():
    with pytest.raises(ValidationError):
        TerminologyMap(
            id="urn:eoip:branding:terminology:t-acme",
            tenant_id="t-acme",
            renames={"Service": "App", "Incident": "app"},
        )


def test_terminology_registry_defaults_to_identity():
    registry = TerminologyRegistry()
    assert registry.rename("t-x", "Service") == "Service"
    registry.register(
        TerminologyMap(
            id="urn:eoip:branding:terminology:t-x",
            tenant_id="t-x",
            renames={"Service": "Application"},
        )
    )
    assert registry.canonicalize("t-x", "Application") == "Service"


# --------------------------------------------------------- localization ---

def test_localization_fallback_chain():
    registry = LocalizationRegistry()
    pack = LocalizationPack(
        id="urn:eoip:branding:locale:fr",
        tenant_id="t-1",
        locale="fr",
        rtl=False,
        strings={"home.title": "Accueil"},
    )
    registry.register(pack)
    assert registry.message("t-1", "fr-CA", "home.title") == "Accueil"
    assert registry.message("t-1", "de", "home.title") == "Accueil"  # any-pack fallback
    assert registry.message("t-2", "fr", "home.title") is None
    assert registry.message("t-2", "fr", "home.title", default="Home") == "Home"


def test_localization_rtl_and_locale_validation():
    pack = LocalizationPack(
        id="urn:eoip:branding:locale:ar",
        tenant_id="t-1",
        locale="ar",
        rtl=True,
    )
    assert pack.rtl is True
    with pytest.raises(ValidationError):
        LocalizationPack(id="urn:eoip:branding:locale:bad", tenant_id="t", locale="not_a_locale!")


# ---------------------------------------------------------------- legal ---

def test_legal_content_registry():
    registry = LegalContentRegistry()
    terms = LegalContentRecord(
        id="urn:eoip:branding:legal:acme-terms",
        tenant_id="t-acme",
        kind=LegalContentKind.TERMS_OF_SERVICE,
        title="Acme Terms",
        version="2.0.0",
        body_markdown="# Terms",
        published=True,
        required=True,
    )
    draft = LegalContentRecord(
        id="urn:eoip:branding:legal:acme-privacy",
        tenant_id="t-acme",
        kind=LegalContentKind.PRIVACY_NOTICE,
        title="Draft privacy",
        published=False,
    )
    registry.register(terms)
    registry.register(draft)
    published = registry.published("t-acme")
    assert [r.id for r in published] == [terms.id]
    assert [r.id for r in registry.required_pending("t-acme")] == [terms.id]


def test_legal_content_url_scheme():
    with pytest.raises(ValidationError):
        LegalContentRecord(
            id="urn:eoip:branding:legal:x",
            tenant_id="t",
            kind=LegalContentKind.HELP_LINK,
            title="help",
            url="http://insecure.example.com",
        )


# ------------------------------------------------------------ devendoring ---

def test_devendoring_checklist():
    overrides = [
        IdentifierOverride(
            identifier_class=cls,
            default_value="eoip",
            override_value="acme",
            external_gate=cls in {IdentifierClass.CLI_BINARY_NAME, IdentifierClass.INSTALLERS},
        )
        for cls in IdentifierClass
    ]
    checklist = DeVendoringChecklist(
        id="urn:eoip:branding:devendor:acme",
        tenant_id="t-acme",
        overrides=overrides,
        powered_by=PoweredByToggle(licensed=False),
    )
    coverage = checklist.coverage()
    assert all(coverage.values())
    assert checklist.complete()
    assert not checklist.powered_by.licensed


def test_devendoring_urn_validation():
    with pytest.raises(ValidationError):
        DeVendoringChecklist(id="checklist-1", tenant_id="t")


# --------------------------------------------------------------- router ---

def test_router_routes():
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    registry = ThemeRegistry(default_theme=_theme())
    app = FastAPI()
    app.include_router(build_router(registry))
    client = TestClient(app)

    resp = client.get("/api/v1/branding/theme")
    assert resp.status_code == 200
    assert resp.json()["app_name"] == "EOIP"

    resp = client.post("/api/v1/branding/terminology/rename", json={"canonical_types": ["Service"]})
    assert resp.json()["renames"] == {"Service": "Service"}

    resp = client.post(
        "/api/v1/branding/terminology/canonicalize", json={"labels": ["Application"]}
    )
    assert resp.json()["canonical"] == {"Application": "Application"}
