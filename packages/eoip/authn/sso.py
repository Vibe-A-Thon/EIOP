"""SSO: OpenID Connect and SAML 2.0 login against an external IdP (FT-AUTH).

Providers live in :mod:`eoip.authn.sso_providers` and are enabled with ``EOIP_SSO_PROVIDER``
(``oidc``, ``saml`` or ``oidc,saml``) plus the settings below; with nothing set, SSO stays
disabled and the disabled stubs below answer (the ``/login`` route returns 501).

Rules every provider follows:

1. ``begin_login`` returns the IdP redirect URL (OIDC: authorization code + PKCE S256 + nonce;
   SAML: AuthnRequest over HTTP-Redirect); ``complete_login`` validates the IdP response
   (signature, issuer, audience, nonce/InResponseTo, expiry, single use) and returns a
   :class:`~eoip.authn.Principal`;
2. the IdP subject must be an explicitly provisioned, enabled principal in the credential store
   (roles stay per-user in EOIP; IdP group claims may only *select* among that user's roles via
   ``EOIP_SSO_GROUP_ROLES`` -- they never create a role);
3. misconfiguration is a startup error (fail closed).

Settings (secrets may be given as ``*_FILE`` paths instead of values):

* OIDC: ``EOIP_OIDC_ISSUER``, ``EOIP_OIDC_CLIENT_ID``, ``EOIP_OIDC_CLIENT_SECRET[_FILE]``,
  ``EOIP_OIDC_REDIRECT_URI``;
* SAML: ``EOIP_SAML_SP_ENTITY_ID``, ``EOIP_SAML_ACS_URL``, ``EOIP_SAML_IDP_METADATA_FILE``;
* both: ``EOIP_SSO_GROUP_ROLES`` -- JSON ``{"idp-group": ["eoip-role", ...]}`` (optional; without
  it a provisioned user signs in with all of their stored roles).

Pending logins (state/nonce/PKCE verifier, AuthnRequest IDs) are kept in process memory, so run
the API as one process or with sticky sessions. See docs/authentication.md.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
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
            f"{self.protocol} SSO is not enabled on this deployment (see EOIP_SSO_PROVIDER); sign in with username/password"
        )

    def begin_login(self, redirect_uri: str, state: str) -> str:
        raise self._unavailable()

    def complete_login(self, params: dict[str, Any]) -> Principal:
        raise self._unavailable()

    def describe(self) -> dict[str, Any]:
        return {"name": self.name, "protocol": self.protocol, "enabled": False, "status": "disabled"}


class OIDCProviderStub(_DisabledProvider):
    """Placeholder for an OpenID Connect provider (authorization code + PKCE). Disabled."""

    name = "oidc"
    protocol = "OIDC"


class SAMLProviderStub(_DisabledProvider):
    """Placeholder for a SAML 2.0 service-provider integration. Disabled."""

    name = "saml"
    protocol = "SAML 2.0"


PROVIDERS: dict[str, Any] = {"oidc": OIDCProviderStub(), "saml": SAMLProviderStub()}
_STUBS = dict(PROVIDERS)

_REQUIRED = {
    "oidc": ("EOIP_OIDC_ISSUER", "EOIP_OIDC_CLIENT_ID", "EOIP_OIDC_REDIRECT_URI"),
    "saml": ("EOIP_SAML_SP_ENTITY_ID", "EOIP_SAML_ACS_URL", "EOIP_SAML_IDP_METADATA_FILE"),
}


def _requested(env: dict[str, str]) -> list[str]:
    return [n.strip().lower() for n in env.get(SSO_PROVIDER_ENV, "").split(",") if n.strip()]


def _secret(env: dict[str, str], name: str) -> str | None:
    if env.get(name + "_FILE"):
        return Path(env[name + "_FILE"]).read_text(encoding="utf-8").strip()
    return env.get(name) or None


def check_sso_configuration() -> None:
    """Fail closed on an unknown provider name or an incomplete provider configuration."""
    _validate(dict(os.environ))


def _validate(env: dict[str, str]) -> None:
    for name in _requested(env):
        if name not in _REQUIRED:
            raise RuntimeError(f"{SSO_PROVIDER_ENV}: unknown SSO provider {name!r} (expected oidc and/or saml)")
        missing = [k for k in _REQUIRED[name] if not env.get(k)]
        if name == "oidc" and not (env.get("EOIP_OIDC_CLIENT_SECRET") or env.get("EOIP_OIDC_CLIENT_SECRET_FILE")):
            missing.append("EOIP_OIDC_CLIENT_SECRET[_FILE]")
        if missing:
            raise RuntimeError(f"{SSO_PROVIDER_ENV} includes {name!r} but {', '.join(missing)} is not set")
    if env.get("EOIP_SSO_GROUP_ROLES"):
        _group_roles(env)


def _group_roles(env: dict[str, str]) -> dict[str, list[str]] | None:
    raw = env.get("EOIP_SSO_GROUP_ROLES")
    if not raw:
        return None
    try:
        value = json.loads(raw)
    except ValueError as exc:
        raise RuntimeError("EOIP_SSO_GROUP_ROLES must be JSON {group: [roles]}") from exc
    if not isinstance(value, dict) or not all(isinstance(v, list) and all(isinstance(r, str) for r in v)
                                              for v in value.values()):
        raise RuntimeError("EOIP_SSO_GROUP_ROLES must be JSON {group: [roles]}")
    return value


def configure_sso(credentials: Any, env: dict[str, str] | None = None) -> dict[str, Any]:
    """Build the enabled providers from the environment and register them in :data:`PROVIDERS`.

    Returns the enabled providers (empty when SSO is off). Unconfigured names keep their
    disabled stub, so ``/login`` for them still answers 501."""
    from eoip.authn.sso_providers import OIDCProvider, SAMLServiceProvider, SubjectMapping, idp_from_metadata

    env = dict(os.environ if env is None else env)
    _validate(env)
    PROVIDERS.clear()
    PROVIDERS.update(_STUBS)
    enabled: dict[str, Any] = {}
    names = _requested(env)
    if not names:
        return enabled
    mapping = SubjectMapping(credentials, group_roles=_group_roles(env))
    for name in names:
        if name == "oidc":
            enabled[name] = OIDCProvider(issuer=env["EOIP_OIDC_ISSUER"], client_id=env["EOIP_OIDC_CLIENT_ID"],
                                         client_secret=_secret(env, "EOIP_OIDC_CLIENT_SECRET"), mapping=mapping)
            enabled[name].redirect_uri = env["EOIP_OIDC_REDIRECT_URI"]
        elif name == "saml":
            idp = idp_from_metadata(Path(env["EOIP_SAML_IDP_METADATA_FILE"]).read_bytes())
            enabled[name] = SAMLServiceProvider(
                sp_entity_id=env["EOIP_SAML_SP_ENTITY_ID"], acs_url=env["EOIP_SAML_ACS_URL"],
                idp_entity_id=idp["entity_id"], idp_sso_url=idp["sso_url"],
                idp_certificate_pem=idp["certificate"], mapping=mapping)
            enabled[name].redirect_uri = env["EOIP_SAML_ACS_URL"]
        else:
            raise RuntimeError(f"{SSO_PROVIDER_ENV}: unknown SSO provider {name!r}")
    PROVIDERS.update(enabled)
    return enabled


def describe_providers() -> list[dict[str, Any]]:
    return [p.describe() for p in PROVIDERS.values()]
