"""SSO placeholder: pluggable provider interface with DISABLED OIDC and SAML stubs (FT-AUTH).

STATUS: PLACEHOLDER -- NOT IMPLEMENTED. No SSO login is possible today.

The interface below is the integration point for a future OIDC (authorization-code +
PKCE) or SAML 2.0 provider. A real provider must:

1. implement :class:`SSOProvider` (``begin_login`` returns the IdP redirect URL;
   ``complete_login`` validates the IdP response -- signature, issuer, audience, nonce,
   expiry -- and returns a :class:`~eoip.authn.Principal`);
2. map the IdP subject to an explicitly provisioned principal in the credential store
   (roles stay per-user in EOIP; IdP group claims may only *select* among roles that an
   administrator has mapped -- they never create a default role);
3. be registered in :data:`PROVIDERS` and enabled with ``EOIP_SSO_PROVIDER=<name>``.

Until then, setting ``EOIP_SSO_PROVIDER`` is a startup error (fail closed), and the
``/api/v1/auth/sso/{name}/login`` route answers 501.
See docs/authentication.md.
"""

from __future__ import annotations

import os
from typing import Any, Protocol, runtime_checkable

from eoip.authn import AuthenticationUnavailable, Principal

SSO_PROVIDER_ENV = "EOIP_SSO_PROVIDER"


@runtime_checkable
class SSOProvider(Protocol):
    name: str
    protocol: str
    enabled: bool

    def begin_login(self, redirect_uri: str, state: str) -> str:
        """Return the IdP authorization/AuthnRequest URL."""
        ...

    def complete_login(self, params: dict[str, Any]) -> Principal:
        """Validate the IdP response and return the provisioned principal."""
        ...


class _DisabledProvider:
    name = ""
    protocol = ""
    enabled = False

    def _unavailable(self) -> AuthenticationUnavailable:
        return AuthenticationUnavailable(
            f"{self.protocol} SSO is a placeholder and not implemented; sign in with username/password"
        )

    def begin_login(self, redirect_uri: str, state: str) -> str:
        raise self._unavailable()

    def complete_login(self, params: dict[str, Any]) -> Principal:
        raise self._unavailable()

    def describe(self) -> dict[str, Any]:
        return {"name": self.name, "protocol": self.protocol, "enabled": False, "status": "placeholder"}


class OIDCProviderStub(_DisabledProvider):
    """Placeholder for an OpenID Connect provider (authorization code + PKCE). Disabled."""

    name = "oidc"
    protocol = "OIDC"


class SAMLProviderStub(_DisabledProvider):
    """Placeholder for a SAML 2.0 service-provider integration. Disabled."""

    name = "saml"
    protocol = "SAML 2.0"


PROVIDERS: dict[str, _DisabledProvider] = {"oidc": OIDCProviderStub(), "saml": SAMLProviderStub()}


def check_sso_configuration() -> None:
    """Fail closed if someone tries to enable a placeholder provider."""
    requested = os.environ.get(SSO_PROVIDER_ENV, "").strip()
    if requested:
        raise RuntimeError(
            f"{SSO_PROVIDER_ENV}={requested!r}: SSO providers are placeholders and cannot be "
            "enabled yet (see docs/authentication.md); unset it and use login credentials"
        )


def describe_providers() -> list[dict[str, Any]]:
    return [p.describe() for p in PROVIDERS.values()]
