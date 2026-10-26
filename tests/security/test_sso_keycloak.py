"""FT-AUTH: OIDC and SAML 2.0 SSO against a real Keycloak (free, Docker).

Requires ``EOIP_LIVE_KEYCLOAK_URL`` plus ``EOIP_LIVE_KEYCLOAK_ADMIN`` / ``EOIP_LIVE_KEYCLOAK_ADMIN_PASSWORD``
(CI starts ``quay.io/keycloak/keycloak`` with a per-run admin password). Each test module creates
its own realm, clients and users with random passwords through the admin REST API, then drives
the real browser flow headlessly (login form POST) and validates the IdP's responses with the
EOIP providers. Skipped when no Keycloak is configured.
"""
from __future__ import annotations

import base64
import html
import os
import re
import secrets
import urllib.parse
import uuid

import pytest

httpx = pytest.importorskip("httpx")
pytest.importorskip("signxml")
from eoip.authn.credentials import CredentialStore
from eoip.authn.sso_providers import (
    OIDCProvider,
    SAMLServiceProvider,
    SSOError,
    SubjectMapping,
    idp_from_metadata,
)
from lxml import etree

KC = os.environ.get("EOIP_LIVE_KEYCLOAK_URL", "").rstrip("/")
pytestmark = [pytest.mark.req("FT-AUTH"),
              pytest.mark.skipif(not KC, reason="EOIP_LIVE_KEYCLOAK_URL not set (no Keycloak)")]

REDIRECT = "http://127.0.0.1:9/api/v1/auth/sso/oidc/callback"
ACS = "http://127.0.0.1:9/api/v1/auth/sso/saml/acs"
SP_ENTITY = "urn:eoip:sp:test"


def _admin_token() -> str:
    r = httpx.post(f"{KC}/realms/master/protocol/openid-connect/token",
                   data={"grant_type": "password", "client_id": "admin-cli",
                         "username": os.environ["EOIP_LIVE_KEYCLOAK_ADMIN"],
                         "password": os.environ["EOIP_LIVE_KEYCLOAK_ADMIN_PASSWORD"]})
    r.raise_for_status()
    return r.json()["access_token"]


@pytest.fixture(scope="module")
def realm(tmp_path_factory):
    name = f"eoip-{uuid.uuid4().hex[:8]}"
    h = {"Authorization": f"Bearer {_admin_token()}"}
    api = f"{KC}/admin/realms"

    def ok(r):
        assert r.status_code < 300, (r.status_code, r.text[:300])
        return r

    ok(httpx.post(api, headers=h, json={"realm": name, "enabled": True, "accessTokenLifespan": 300}))
    ok(httpx.post(f"{api}/{name}/clients", headers=h, json={
        "clientId": "eoip", "protocol": "openid-connect", "publicClient": False, "standardFlowEnabled": True,
        "directAccessGrantsEnabled": False, "redirectUris": [REDIRECT],
        "attributes": {"pkce.code.challenge.method": "S256"},
        "protocolMappers": [{"name": "groups", "protocol": "openid-connect", "protocolMapper": "oidc-group-membership-mapper",
                             "config": {"claim.name": "groups", "full.path": "false", "id.token.claim": "true",
                                        "access.token.claim": "false", "userinfo.token.claim": "true"}}]}))
    cid = ok(httpx.get(f"{api}/{name}/clients", headers=h, params={"clientId": "eoip"})).json()[0]["id"]
    secret = ok(httpx.get(f"{api}/{name}/clients/{cid}/client-secret", headers=h)).json()["value"]
    ok(httpx.post(f"{api}/{name}/clients", headers=h, json={
        "clientId": SP_ENTITY, "protocol": "saml", "redirectUris": [ACS], "frontchannelLogout": False,
        "attributes": {"saml.server.signature": "true", "saml.assertion.signature": "false",
                       "saml.client.signature": "false", "saml.authnstatement": "true",
                       "saml_name_id_format": "username", "saml.force.name.id.format": "true",
                       "saml_assertion_consumer_url_post": ACS, "saml.signature.algorithm": "RSA_SHA256"},
        "protocolMappers": [{"name": "groups", "protocol": "saml", "protocolMapper": "saml-group-membership-mapper",
                             "config": {"attribute.name": "groups", "full.path": "false", "single": "false"}}]}))
    for g in ("eoip-analysts", "eoip-admins", "unmapped"):
        ok(httpx.post(f"{api}/{name}/groups", headers=h, json={"name": g}))
    groups = {g["name"]: g["id"] for g in ok(httpx.get(f"{api}/{name}/groups", headers=h)).json()}
    users = {}
    for user, member_of in (("alice", ["eoip-analysts"]), ("carol", ["unmapped"]), ("mallory", ["eoip-admins"])):
        pw = secrets.token_urlsafe(18)
        ok(httpx.post(f"{api}/{name}/users", headers=h, json={
            "username": user, "enabled": True, "email": f"{user}@example.test", "emailVerified": True,
            "firstName": user, "lastName": "Test", "credentials": [{"type": "password", "value": pw, "temporary": False}]}))
        uid = ok(httpx.get(f"{api}/{name}/users", headers=h, params={"username": user, "exact": "true"})).json()[0]["id"]
        for g in member_of:
            ok(httpx.put(f"{api}/{name}/users/{uid}/groups/{groups[g]}", headers=h))
        users[user] = pw
    store = CredentialStore(tmp_path_factory.mktemp("sso") / "creds.json")
    store.create_user("alice", None, ["analyst", "viewer"], tenant_id="acme")  # SSO-only principals, no password
    store.create_user("carol", None, ["analyst"], tenant_id="acme")
    mapping = SubjectMapping(store, group_roles={"eoip-analysts": ["analyst"], "eoip-admins": ["admin"]})
    yield {"name": name, "issuer": f"{KC}/realms/{name}", "secret": secret, "users": users, "mapping": mapping}
    httpx.delete(f"{api}/{name}", headers={"Authorization": f"Bearer {_admin_token()}"})


def _login(url: str, user: str, password: str) -> httpx.Response:
    """Headless browser: load the IdP login page and submit the credentials form."""
    with httpx.Client(follow_redirects=False, timeout=20) as b:
        r = b.get(url, follow_redirects=True)
        assert r.status_code == 200, r.text[:300]
        for c in b.cookies.jar:  # Keycloak marks its cookies Secure; browsers treat http://localhost as secure
            c.secure = False
        action = html.unescape(re.search(r'<form[^>]+id="kc-form-login"[^>]+action="([^"]+)"', r.text).group(1))
        return b.post(action, data={"username": user, "password": password, "credentialId": ""})


def _code(resp: httpx.Response) -> dict[str, str]:
    assert resp.status_code in (302, 303), resp.text[:300]
    loc = resp.headers["location"]
    assert loc.startswith(REDIRECT), loc
    return dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(loc).query))


def _saml_post(resp: httpx.Response) -> dict[str, str]:
    assert resp.status_code == 200, resp.text[:300]
    fields = dict(re.findall(r'name="(SAMLResponse|RelayState)"\s+value="([^"]*)"', resp.text))
    return {k: html.unescape(v) for k, v in fields.items()}


# ----------------------------------------------------------------------------------------------- OIDC

def _oidc(realm, secret=None):
    return OIDCProvider(issuer=realm["issuer"], client_id="eoip", client_secret=secret or realm["secret"],
                        mapping=realm["mapping"])


def test_oidc_code_flow_with_pkce_maps_to_provisioned_principal(realm):
    rp = _oidc(realm)
    state = secrets.token_urlsafe(24)
    url = rp.begin_login(REDIRECT, state)
    q = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query))
    assert q["code_challenge_method"] == "S256" and q["nonce"] and q["state"] == state
    params = _code(_login(url, "alice", realm["users"]["alice"]))
    p = rp.complete_login(params)
    assert (p.username, p.provider, p.tenant_id, p.roles) == ("alice", "oidc", "acme", ("analyst",))
    assert p.claims["iss"] == realm["issuer"] and "id_token" not in repr(p)
    with pytest.raises(SSOError, match="unknown or already used"):
        rp.complete_login(params)  # state is single use


def test_oidc_refuses_unprovisioned_users_and_unselected_roles(realm):
    rp = _oidc(realm)
    for user, msg in (("mallory", "not provisioned"), ("carol", "none of the user's EOIP roles")):
        state = secrets.token_urlsafe(24)
        params = _code(_login(rp.begin_login(REDIRECT, state), user, realm["users"][user]))
        with pytest.raises(SSOError, match=msg):
            rp.complete_login(params)


def test_oidc_rejects_wrong_secret_forged_state_and_tampered_tokens(realm):
    rp = _oidc(realm, secret="not-the-secret")
    state = secrets.token_urlsafe(24)
    params = _code(_login(rp.begin_login(REDIRECT, state), "alice", realm["users"]["alice"]))
    with pytest.raises(SSOError, match="refused the code exchange"):
        rp.complete_login(params)
    with pytest.raises(SSOError, match="unknown or already used"):
        _oidc(realm).complete_login({"state": secrets.token_urlsafe(24), "code": "x"})
    # Get a genuine ID token, then tamper with it.
    good = _oidc(realm)
    state = secrets.token_urlsafe(24)
    url = good.begin_login(REDIRECT, state)
    nonce = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query))["nonce"]
    params = _code(_login(url, "alice", realm["users"]["alice"]))
    pending = good._pending.pop(state)
    tok = httpx.post(good.discovery()["token_endpoint"], auth=("eoip", realm["secret"]), data={
        "grant_type": "authorization_code", "code": params["code"], "redirect_uri": REDIRECT,
        "code_verifier": pending["verifier"]}).json()["id_token"]
    assert good.validate_id_token(tok, nonce)["preferred_username"] == "alice"
    with pytest.raises(SSOError, match="nonce"):
        good.validate_id_token(tok, "other-nonce")
    h, b, s = tok.split(".")
    payload = base64.urlsafe_b64decode(b + "=" * (-len(b) % 4)).replace(b'"alice"', b'"admin"')
    forged = ".".join([h, base64.urlsafe_b64encode(payload).decode().rstrip("="), s])
    with pytest.raises(SSOError, match="signature"):
        good.validate_id_token(forged, nonce)
    other = OIDCProvider(issuer=realm["issuer"], client_id="someone-else", client_secret=None, mapping=realm["mapping"])
    with pytest.raises(SSOError, match="audience"):
        other.validate_id_token(tok, nonce)


# ----------------------------------------------------------------------------------------------- SAML

def _sp(realm, **kw):
    md = httpx.get(f"{realm['issuer']}/protocol/saml/descriptor")
    md.raise_for_status()
    idp = idp_from_metadata(md.content)
    args = {"sp_entity_id": SP_ENTITY, "acs_url": ACS, "idp_entity_id": idp["entity_id"], "idp_sso_url": idp["sso_url"],
            "idp_certificate_pem": idp["certificate"], "mapping": realm["mapping"]}
    args.update(kw)
    return SAMLServiceProvider(**args)


def test_saml_sp_initiated_login_with_signed_response(realm):
    sp = _sp(realm)
    state = secrets.token_urlsafe(24)
    form = _saml_post(_login(sp.begin_login(ACS, state), "alice", realm["users"]["alice"]))
    assert form["RelayState"] == state
    p = sp.complete_login(form)
    assert (p.username, p.provider, p.tenant_id, p.roles) == ("alice", "saml", "acme", ("analyst",))
    with pytest.raises(SSOError, match="unknown or already used"):
        sp.complete_login(form)  # replay of the same response


def test_saml_rejects_tampering_wrapping_audience_and_expiry(realm):
    sp = _sp(realm)
    state = secrets.token_urlsafe(24)
    form = _saml_post(_login(sp.begin_login(ACS, state), "alice", realm["users"]["alice"]))
    xml = base64.b64decode(form["SAMLResponse"])
    req_id = etree.fromstring(xml).get("InResponseTo")

    def again(data: bytes) -> dict[str, str]:
        sp._pending.put(req_id, {"state": state})  # re-arm the transaction to test each attack in isolation
        return {"SAMLResponse": base64.b64encode(data).decode(), "RelayState": state}

    # 1. Tampered NameID breaks the signature.
    with pytest.raises(SSOError, match="signature"):
        sp.complete_login(again(xml.replace(b">alice<", b">carol<")))
    # 2. Signature wrapping: an unsigned evil assertion placed before the signed one is never read.
    root = etree.fromstring(xml)
    ns = {"saml": "urn:oasis:names:tc:SAML:2.0:assertion"}
    evil = etree.fromstring(etree.tostring(root.find("saml:Assertion", ns)))
    evil.set("ID", "_evil")
    evil.find(".//saml:NameID", ns).text = "carol"
    root.insert(list(root).index(root.find("saml:Assertion", ns)), evil)
    with pytest.raises(SSOError, match="signature"):  # Keycloak signs the whole Response: injection breaks it
        sp.complete_login(again(etree.tostring(root)))
    # 2b. Classic XSW: an evil unsigned Response wraps the genuine signed one; only the signed element is read.
    outer = etree.fromstring(xml)
    wrapper = etree.fromstring(etree.tostring(outer))
    for child in list(wrapper):
        wrapper.remove(child)
    wrapper.set("ID", "_wrapper")
    ev = etree.fromstring(etree.tostring(outer.find("saml:Assertion", ns)))
    ev.find(".//saml:NameID", ns).text = "carol"
    wrapper.append(etree.fromstring(etree.tostring(outer.find("{urn:oasis:names:tc:SAML:2.0:protocol}Status"))))
    wrapper.append(ev)
    ext = etree.SubElement(wrapper, "{urn:oasis:names:tc:SAML:2.0:protocol}Extensions")
    ext.append(outer)
    try:
        p = sp.complete_login(again(etree.tostring(wrapper)))
        assert p.username == "alice"  # never the attacker's carol
    except SSOError:
        pass  # refusing the wrapped document is equally safe
    # 3. A different SP (audience) and an expired clock are refused, while the genuine response verifies.
    wrong_aud = _sp(realm, sp_entity_id="urn:eoip:sp:other")
    wrong_aud._pending.put(req_id, {"state": state})
    with pytest.raises(SSOError, match="audience"):
        wrong_aud.complete_login({"SAMLResponse": form["SAMLResponse"], "RelayState": state})
    import time as _t
    late = _sp(realm, now=lambda: _t.time() + 3600)
    late._pending = sp._pending.__class__(ttl=7200, now=late._now)
    late._pending.put(req_id, {"state": state})
    with pytest.raises(SSOError, match="expired|SubjectConfirmation"):
        late.complete_login({"SAMLResponse": form["SAMLResponse"], "RelayState": state})
    # 4. Unsolicited response (no matching AuthnRequest) is refused.
    with pytest.raises(SSOError, match="unknown or already used"):
        _sp(realm).complete_login({"SAMLResponse": form["SAMLResponse"]})
    # 5. Wrong IdP certificate.
    import datetime as dt

    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.x509.oid import NameOID
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    nm = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "attacker")])
    cert = (x509.CertificateBuilder().subject_name(nm).issuer_name(nm).public_key(key.public_key())
            .serial_number(1).not_valid_before(dt.datetime(2020, 1, 1)).not_valid_after(dt.datetime(2040, 1, 1))
            .sign(key, hashes.SHA256()))
    bad = _sp(realm, idp_certificate_pem=cert.public_bytes(serialization.Encoding.PEM).decode())
    bad._pending.put(req_id, {"state": state})
    with pytest.raises(SSOError, match="signature"):
        bad.complete_login({"SAMLResponse": form["SAMLResponse"], "RelayState": state})


# ----------------------------------------------------------------------------------------------- API

def test_api_sso_routes_issue_sessions_with_the_selected_roles(realm, tmp_path, monkeypatch):
    """End to end through the FastAPI app: /login -> Keycloak -> callback/ACS -> EOIP session."""
    from eoip.graph.memory import MemoryGraphStore
    from fastapi.testclient import TestClient

    import apps.api.main as api_main

    for key in ("EOIP_ASG_FILE", "EOIP_API_TOKEN", "EOIP_CREDENTIALS_FILE"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setattr(api_main, "create_store", MemoryGraphStore)
    monkeypatch.setattr(api_main, "data_root", lambda: tmp_path)
    store = CredentialStore(tmp_path / "state" / "credentials.json")
    store.create_user("alice", None, ["analyst", "viewer"], tenant_id="acme")
    secret_file = tmp_path / "oidc.secret"
    secret_file.write_text(realm["secret"], encoding="utf-8")
    md = tmp_path / "idp.xml"
    md.write_bytes(httpx.get(f"{realm['issuer']}/protocol/saml/descriptor").content)
    for k, v in {"EOIP_SESSION_SECRET": secrets.token_urlsafe(40), "EOIP_SSO_PROVIDER": "oidc,saml",
                 "EOIP_OIDC_ISSUER": realm["issuer"], "EOIP_OIDC_CLIENT_ID": "eoip",
                 "EOIP_OIDC_CLIENT_SECRET_FILE": str(secret_file), "EOIP_OIDC_REDIRECT_URI": REDIRECT,
                 "EOIP_SAML_SP_ENTITY_ID": SP_ENTITY, "EOIP_SAML_ACS_URL": ACS, "EOIP_SAML_IDP_METADATA_FILE": str(md),
                 "EOIP_SSO_GROUP_ROLES": '{"eoip-analysts": ["analyst"], "eoip-admins": ["admin"]}'}.items():
        monkeypatch.setenv(k, v)
    with TestClient(api_main.create_app()) as c:
        sso = {p["name"]: p["enabled"] for p in c.get("/api/v1/auth/providers").json()["sso"]}
        assert sso == {"oidc": True, "saml": True}
        # OIDC
        r = c.get("/api/v1/auth/sso/oidc/login", follow_redirects=False)
        assert r.status_code == 302 and r.headers["location"].startswith(realm["issuer"])
        params = _code(_login(r.headers["location"], "alice", realm["users"]["alice"]))
        r = c.get("/api/v1/auth/sso/oidc/callback", params=params)
        assert r.status_code == 200, r.text
        token = r.json()["token"]
        me = c.get("/api/v1/auth/whoami", headers={"Authorization": f"Bearer {token}"}).json()
        assert (me["username"], me["roles"], me["tenant_id"], me["provider"]) == ("alice", ["analyst"], "acme", "oidc")
        assert c.get("/api/v1/auth/sso/oidc/callback", params=params).status_code == 401  # replay
        # SAML
        r = c.get("/api/v1/auth/sso/saml/login", follow_redirects=False)
        form = _saml_post(_login(r.headers["location"], "alice", realm["users"]["alice"]))
        r = c.post("/api/v1/auth/sso/saml/acs", data=form)
        assert r.status_code == 200, r.text
        saml_token = r.json()["token"]
        me = c.get("/api/v1/auth/whoami", headers={"Authorization": f"Bearer {saml_token}"}).json()
        assert (me["roles"], me["provider"]) == (["analyst"], "saml")
        # Revocation in EOIP applies to live SSO sessions at once; nothing is ever added.
        store.set_roles("alice", ["viewer", "admin"])
        assert c.get("/api/v1/auth/whoami", headers={"Authorization": f"Bearer {token}"}).status_code == 401
        store.set_roles("alice", ["analyst", "admin"])
        me = c.get("/api/v1/auth/whoami", headers={"Authorization": f"Bearer {token}"}).json()
        assert me["roles"] == ["analyst"]
        store.set_enabled("alice", False)
        assert c.get("/api/v1/auth/whoami", headers={"Authorization": f"Bearer {saml_token}"}).status_code == 401
