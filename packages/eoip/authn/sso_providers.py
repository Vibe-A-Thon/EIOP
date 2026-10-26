"""OIDC (authorization code + PKCE) and SAML 2.0 (SP-initiated, HTTP-Redirect/POST) SSO providers (FT-AUTH).

Both providers follow the rules in :mod:`eoip.authn.sso`:

* The IdP response is fully validated before anything is trusted. OIDC: single-use ``state``,
  PKCE S256 code exchange, ID-token RS256 signature against the IdP JWKS (refetched once on an
  unknown ``kid`` for key rotation), ``iss``/``aud``/``azp``/``exp``/``nbf``/``nonce``. SAML: single-use
  ``InResponseTo`` bound to the AuthnRequest, XML signature against the configured IdP certificate
  (only the signed element is read, which defeats signature-wrapping), ``Issuer``, ``Destination``,
  ``Conditions`` validity window, ``AudienceRestriction``, bearer ``SubjectConfirmationData``.
* The IdP subject is mapped to a principal that an administrator already provisioned in the
  credential store (``eoip-admin add-user`` with no password). There is no just-in-time
  provisioning; unknown or disabled users are refused.
* IdP group claims can only *select* among the roles stored for that user (``group_roles`` maps an
  IdP group to EOIP roles; the effective roles are the intersection). They never add a role.
"""
from __future__ import annotations

import base64
import hashlib
import secrets
import threading
import time
import urllib.parse
import zlib
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from eoip.authn import (
    AuthenticationError,
    OidcJwtValidator,
    Principal,
    TokenError,
    _b64u_decode,
)

_DEFAULT_TTL = 600.0


class SSOError(AuthenticationError):
    """The IdP response was rejected. The message is safe to show; it never contains tokens."""


class _PendingLogins:
    """Single-use, expiring login transactions keyed by state / request id."""

    def __init__(self, ttl: float = _DEFAULT_TTL, now: Callable[[], float] = time.time) -> None:
        self._ttl, self._now = ttl, now
        self._items: dict[str, tuple[float, dict[str, Any]]] = {}
        self._lock = threading.Lock()

    def put(self, key: str, value: dict[str, Any]) -> None:
        with self._lock:
            now = self._now()
            self._items = {k: v for k, v in self._items.items() if v[0] > now}
            self._items[key] = (now + self._ttl, value)

    def pop(self, key: str) -> dict[str, Any]:
        with self._lock:
            item = self._items.pop(key or "", None)
        if item is None:
            raise SSOError("unknown or already used login transaction")
        if item[0] <= self._now():
            raise SSOError("login transaction expired")
        return item[1]


@dataclass
class SubjectMapping:
    """Maps a validated IdP identity to a provisioned EOIP principal."""

    credential_store: Any
    group_roles: dict[str, list[str]] = field(default_factory=dict)

    def principal(self, provider: str, username: str, groups: list[str], claims: dict[str, Any]) -> Principal:
        record = self.credential_store.get(username)
        if record is None or not record.enabled:
            raise SSOError("the identity provider user is not provisioned in EOIP")
        stored = tuple(record.roles)
        roles = stored
        if self.group_roles:
            selected = {r for g in groups for r in self.group_roles.get(g, [])}
            roles = tuple(r for r in stored if r in selected)
            if not roles:
                raise SSOError("none of the user's EOIP roles is selected by their identity-provider groups")
        p = record.principal(provider, roles)
        return Principal(id=p.id, username=p.username, roles=p.roles, provider=provider, tenant_id=p.tenant_id,
                         claims={k: v for k, v in claims.items() if k in ("iss", "sub", "email", "session_index")})


def _http(client: Any | None):
    if client is not None:
        return client
    import httpx

    return httpx.Client(timeout=10.0, follow_redirects=False)


# --------------------------------------------------------------------------------------------- OIDC


class OIDCProvider:
    """OpenID Connect relying party: authorization code flow with PKCE (S256) and nonce."""

    name = "oidc"
    protocol = "OIDC"
    enabled = True

    def __init__(self, *, issuer: str, client_id: str, client_secret: str | None, mapping: SubjectMapping,
                 http_client: Any = None, scopes: str = "openid profile email",
                 username_claim: str = "preferred_username", groups_claim: str = "groups",
                 leeway_seconds: int = 30, ttl: float = _DEFAULT_TTL) -> None:
        if not issuer or not client_id:
            raise ValueError("issuer and client_id are required")
        self.issuer, self.client_id, self._secret = issuer.rstrip("/"), client_id, client_secret
        self.mapping, self.scopes = mapping, scopes
        self.username_claim, self.groups_claim, self.leeway = username_claim, groups_claim, leeway_seconds
        self._http = _http(http_client)
        self._pending = _PendingLogins(ttl)
        self._config: dict[str, Any] | None = None
        self._jwks: dict[str, Any] | None = None

    def discovery(self) -> dict[str, Any]:
        if self._config is None:
            r = self._http.get(f"{self.issuer}/.well-known/openid-configuration")
            r.raise_for_status()
            cfg = r.json()
            if cfg.get("issuer", "").rstrip("/") != self.issuer:
                raise SSOError("discovery document issuer does not match the configured issuer")
            if "S256" not in cfg.get("code_challenge_methods_supported", ["S256"]):
                raise SSOError("identity provider does not support PKCE S256")
            self._config = cfg
        return self._config

    def _jwks_doc(self, refresh: bool = False) -> dict[str, Any]:
        if self._jwks is None or refresh:
            r = self._http.get(self.discovery()["jwks_uri"])
            r.raise_for_status()
            self._jwks = r.json()
        return self._jwks

    def begin_login(self, redirect_uri: str, state: str) -> str:
        if not state or len(state) < 16:
            raise ValueError("state must be an unguessable value of at least 16 characters")
        verifier = secrets.token_urlsafe(48)
        challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).decode().rstrip("=")
        nonce = secrets.token_urlsafe(24)
        self._pending.put(state, {"verifier": verifier, "nonce": nonce, "redirect_uri": redirect_uri})
        q = {"response_type": "code", "client_id": self.client_id, "redirect_uri": redirect_uri, "scope": self.scopes,
             "state": state, "nonce": nonce, "code_challenge": challenge, "code_challenge_method": "S256"}
        return f"{self.discovery()['authorization_endpoint']}?{urllib.parse.urlencode(q)}"

    def complete_login(self, params: dict[str, Any]) -> Principal:
        pending = self._pending.pop(str(params.get("state") or ""))  # single use, even on IdP error
        if params.get("error"):
            raise SSOError(f"identity provider returned error {str(params['error'])[:64]!r}")
        code = str(params.get("code") or "")
        if not code:
            raise SSOError("authorization response has no code")
        form = {"grant_type": "authorization_code", "code": code, "redirect_uri": pending["redirect_uri"],
                "code_verifier": pending["verifier"], "client_id": self.client_id}
        auth = (self.client_id, self._secret) if self._secret else None
        r = self._http.post(self.discovery()["token_endpoint"], data=form, auth=auth)
        if r.status_code != 200:
            raise SSOError(f"token endpoint refused the code exchange (HTTP {r.status_code})")
        id_token = r.json().get("id_token")
        if not id_token:
            raise SSOError("token response has no id_token")
        claims = self.validate_id_token(id_token, pending["nonce"])
        username = str(claims.get(self.username_claim) or "")
        groups = claims.get(self.groups_claim) or []
        groups = [groups] if isinstance(groups, str) else [str(g).lstrip("/") for g in groups]
        return self.mapping.principal("oidc", username, groups, {**claims, "iss": self.issuer})

    def validate_id_token(self, id_token: str, nonce: str) -> dict[str, Any]:
        import json

        try:
            header = json.loads(_b64u_decode(id_token.split(".")[0]))
            claims = json.loads(_b64u_decode(id_token.split(".")[1]))
        except (ValueError, IndexError) as exc:
            raise SSOError("malformed id_token") from exc
        jwks = self._jwks_doc()
        if header.get("kid") not in {k.get("kid") for k in jwks.get("keys", [])}:
            jwks = self._jwks_doc(refresh=True)  # key rotation
        validator = OidcJwtValidator(issuer=self.issuer, audience=self.client_id, jwks=jwks,
                                     leeway_seconds=self.leeway)
        try:
            validator.validate(id_token)
        except TokenError as exc:
            raise SSOError(f"id_token rejected: {exc}") from exc
        aud = claims.get("aud")
        if isinstance(aud, list) and len(aud) > 1 and claims.get("azp") != self.client_id:
            raise SSOError("id_token azp does not match the client")
        if not nonce or not secrets.compare_digest(str(claims.get("nonce") or ""), nonce):
            raise SSOError("id_token nonce mismatch (replay)")
        return claims

    def describe(self) -> dict[str, Any]:
        return {"name": self.name, "protocol": self.protocol, "enabled": True, "issuer": self.issuer,
                "client_id": self.client_id}


# --------------------------------------------------------------------------------------------- SAML

_NS = {"samlp": "urn:oasis:names:tc:SAML:2.0:protocol", "saml": "urn:oasis:names:tc:SAML:2.0:assertion",
       "ds": "http://www.w3.org/2000/09/xmldsig#", "md": "urn:oasis:names:tc:SAML:2.0:metadata"}
_SUCCESS = "urn:oasis:names:tc:SAML:2.0:status:Success"


def _saml_time(value: str | None) -> float | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()


def _instant(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def idp_from_metadata(xml: bytes | str) -> dict[str, str]:
    """Extract entityID, SSO (HTTP-Redirect) URL and signing certificate from IdP metadata."""
    from lxml import etree

    parser = etree.XMLParser(resolve_entities=False, no_network=True, huge_tree=False)
    root = etree.fromstring(xml.encode() if isinstance(xml, str) else xml, parser=parser)
    ed = root if root.tag == f"{{{_NS['md']}}}EntityDescriptor" else root.find(".//md:EntityDescriptor", _NS)
    idp = ed.find("md:IDPSSODescriptor", _NS)
    sso = next(e.get("Location") for e in idp.findall("md:SingleSignOnService", _NS)
               if e.get("Binding", "").endswith("HTTP-Redirect"))
    cert = None
    for kd in idp.findall("md:KeyDescriptor", _NS):
        if kd.get("use") in (None, "signing"):
            cert = kd.find(".//ds:X509Certificate", _NS).text.strip()
            break
    if not cert:
        raise SSOError("IdP metadata has no signing certificate")
    pem = "-----BEGIN CERTIFICATE-----\n" + "\n".join(
        cert.replace("\n", "")[i:i + 64] for i in range(0, len(cert.replace("\n", "")), 64)) + "\n-----END CERTIFICATE-----\n"
    return {"entity_id": ed.get("entityID"), "sso_url": sso, "certificate": pem}


class SAMLServiceProvider:
    """SAML 2.0 service provider: SP-initiated AuthnRequest (HTTP-Redirect), Response via HTTP-POST."""

    name = "saml"
    protocol = "SAML 2.0"
    enabled = True

    def __init__(self, *, sp_entity_id: str, acs_url: str, idp_entity_id: str, idp_sso_url: str,
                 idp_certificate_pem: str, mapping: SubjectMapping, groups_attribute: str = "groups",
                 leeway_seconds: int = 60, ttl: float = _DEFAULT_TTL, now: Callable[[], float] = time.time) -> None:
        self.sp_entity_id, self.acs_url = sp_entity_id, acs_url
        self.idp_entity_id, self.idp_sso_url, self._cert = idp_entity_id, idp_sso_url, idp_certificate_pem
        self.mapping, self.groups_attribute, self.leeway, self._now = mapping, groups_attribute, leeway_seconds, now
        self._pending = _PendingLogins(ttl, now)

    def begin_login(self, redirect_uri: str, state: str) -> str:
        """``redirect_uri`` is ignored: SAML responses always go to the configured ACS URL."""
        if not state or len(state) < 16:
            raise ValueError("state must be an unguessable value of at least 16 characters")
        req_id = "_" + secrets.token_hex(20)
        self._pending.put(req_id, {"state": state})
        xml = (f'<samlp:AuthnRequest xmlns:samlp="{_NS["samlp"]}" xmlns:saml="{_NS["saml"]}" ID="{req_id}" '
               f'Version="2.0" IssueInstant="{_instant(self._now())}" Destination="{_xml_attr(self.idp_sso_url)}" '
               f'AssertionConsumerServiceURL="{_xml_attr(self.acs_url)}" '
               f'ProtocolBinding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST">'
               f'<saml:Issuer>{_xml_text(self.sp_entity_id)}</saml:Issuer>'
               f'<samlp:NameIDPolicy Format="urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified" AllowCreate="false"/>'
               f'</samlp:AuthnRequest>')
        deflated = zlib.compress(xml.encode())[2:-4]  # raw DEFLATE per the HTTP-Redirect binding
        q = {"SAMLRequest": base64.b64encode(deflated).decode(), "RelayState": state}
        sep = "&" if "?" in self.idp_sso_url else "?"
        return f"{self.idp_sso_url}{sep}{urllib.parse.urlencode(q)}"

    def complete_login(self, params: dict[str, Any]) -> Principal:
        from lxml import etree
        from signxml import XMLVerifier
        from signxml.exceptions import InvalidInput, InvalidSignature

        raw = str(params.get("SAMLResponse") or "")
        if not raw or len(raw) > 512_000:
            raise SSOError("missing or oversized SAMLResponse")
        try:
            xml = base64.b64decode(raw, validate=True)
        except ValueError as exc:
            raise SSOError("SAMLResponse is not base64") from exc
        parser = etree.XMLParser(resolve_entities=False, no_network=True, huge_tree=False)
        try:
            unsigned_root = etree.fromstring(xml, parser=parser)
        except etree.XMLSyntaxError as exc:
            raise SSOError("SAMLResponse is not well-formed XML") from exc
        req_id = unsigned_root.get("InResponseTo") or ""
        pending = self._pending.pop(req_id)  # single use: replays and unsolicited responses are refused
        if params.get("RelayState") is not None and params.get("RelayState") != pending["state"]:
            raise SSOError("RelayState does not match the login transaction")
        try:
            verified = XMLVerifier().verify(xml, x509_cert=self._cert, expect_references=1)
        except (InvalidSignature, InvalidInput) as exc:
            raise SSOError("SAML signature verification failed") from exc
        signed = verified.signed_xml  # read ONLY the signed element from here on (XSW defence)
        if signed.tag == f"{{{_NS['samlp']}}}Response":
            response, assertion = signed, signed.find("saml:Assertion", _NS)
            status = response.find("samlp:Status/samlp:StatusCode", _NS)
            if status is None or status.get("Value") != _SUCCESS:
                raise SSOError("SAML status is not Success")
            if response.get("InResponseTo") != req_id:
                raise SSOError("InResponseTo mismatch")
            if response.get("Destination") not in (None, self.acs_url):
                raise SSOError("Destination mismatch")
            issuer = response.findtext("saml:Issuer", namespaces=_NS)
            if issuer is not None and issuer.strip() != self.idp_entity_id:
                raise SSOError("Response issuer mismatch")
        elif signed.tag == f"{{{_NS['saml']}}}Assertion":
            assertion = signed
            status = unsigned_root.find("samlp:Status/samlp:StatusCode", _NS)
            if status is None or status.get("Value") != _SUCCESS:
                raise SSOError("SAML status is not Success")
        else:
            raise SSOError("signature does not cover a Response or Assertion")
        if assertion is None:
            raise SSOError("no assertion in the signed response")
        return self._principal_from_assertion(assertion, req_id)

    def _principal_from_assertion(self, a: Any, req_id: str) -> Principal:
        now = self._now()
        if (a.findtext("saml:Issuer", namespaces=_NS) or "").strip() != self.idp_entity_id:
            raise SSOError("Assertion issuer mismatch")
        cond = a.find("saml:Conditions", _NS)
        if cond is None:
            raise SSOError("Assertion has no Conditions")
        nb, noa = _saml_time(cond.get("NotBefore")), _saml_time(cond.get("NotOnOrAfter"))
        if nb is not None and now + self.leeway < nb:
            raise SSOError("Assertion not yet valid")
        if noa is None or now - self.leeway >= noa:
            raise SSOError("Assertion expired")
        audiences = [e.text.strip() for e in cond.findall("saml:AudienceRestriction/saml:Audience", _NS) if e.text]
        if self.sp_entity_id not in audiences:
            raise SSOError("Assertion audience does not include this service provider")
        subj = a.find("saml:Subject", _NS)
        name_id = (subj.findtext("saml:NameID", namespaces=_NS) or "").strip() if subj is not None else ""
        if not name_id:
            raise SSOError("Assertion has no NameID")
        ok = False
        for sc in subj.findall("saml:SubjectConfirmation", _NS):
            if sc.get("Method") != "urn:oasis:names:tc:SAML:2.0:cm:bearer":
                continue
            d = sc.find("saml:SubjectConfirmationData", _NS)
            if d is None:
                continue
            exp = _saml_time(d.get("NotOnOrAfter"))
            ok = (d.get("Recipient") == self.acs_url and d.get("InResponseTo") in (None, req_id)
                  and exp is not None and now - self.leeway < exp)
            if ok:
                break
        if not ok:
            raise SSOError("no valid bearer SubjectConfirmation for this ACS")
        groups: list[str] = []
        for attr in a.findall("saml:AttributeStatement/saml:Attribute", _NS):
            if attr.get("Name") in (self.groups_attribute, "Role"):
                groups += [(v.text or "").strip().lstrip("/") for v in attr.findall("saml:AttributeValue", _NS)]
        session = a.find("saml:AuthnStatement", _NS)
        claims = {"iss": self.idp_entity_id, "sub": name_id,
                  "session_index": session.get("SessionIndex") if session is not None else None}
        return self.mapping.principal("saml", name_id, groups, claims)

    def describe(self) -> dict[str, Any]:
        return {"name": self.name, "protocol": self.protocol, "enabled": True, "idp_entity_id": self.idp_entity_id,
                "sp_entity_id": self.sp_entity_id, "acs_url": self.acs_url}


def _xml_attr(v: str) -> str:
    return v.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def _xml_text(v: str) -> str:
    return v.replace("&", "&amp;").replace("<", "&lt;")
