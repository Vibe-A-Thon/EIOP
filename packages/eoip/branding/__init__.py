"""EOIP white-label branding (SR-WL-001/003/004/006/007, SR-ONT-007).

Theme packages (brand tokens + per-tenant resolution), tenant terminology
rename maps (canonical types never change, SR-ONT-007), localization packs,
custom legal/onboarding content, and the de-vendoring checklist model.

De-vendoring of shipped binaries/images/installers is External gate
(release tooling); "powered by" attribution is a licensed toggle.
"""

from eoip.branding.content import LegalContentKind, LegalContentRecord, LegalContentRegistry
from eoip.branding.devendoring import (
    DeVendoringChecklist,
    IdentifierClass,
    IdentifierOverride,
    PoweredByToggle,
)
from eoip.branding.localization import DateNumberFormats, LocalizationPack, LocalizationRegistry
from eoip.branding.terminology import TerminologyMap, TerminologyRegistry
from eoip.branding.theme import (
    AssistantPersona,
    ColorPalette,
    EdgeStyle,
    LogoRef,
    NodeStyle,
    Spacing,
    ThemeMode,
    ThemePackage,
    ThemeRegistry,
    ThemeVariant,
    Typography,
)

__all__ = [
    "AssistantPersona",
    "ColorPalette",
    "DateNumberFormats",
    "DeVendoringChecklist",
    "EdgeStyle",
    "IdentifierClass",
    "IdentifierOverride",
    "LegalContentKind",
    "LegalContentRecord",
    "LegalContentRegistry",
    "LocalizationPack",
    "LocalizationRegistry",
    "LogoRef",
    "NodeStyle",
    "PoweredByToggle",
    "Spacing",
    "TerminologyMap",
    "TerminologyRegistry",
    "ThemeMode",
    "ThemePackage",
    "ThemeRegistry",
    "ThemeVariant",
    "Typography",
]
