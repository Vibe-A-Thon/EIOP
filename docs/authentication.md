# Authentication and roles

FT-AUTH. EOIP has **no default or bootstrap account and no implicit role**. Every request
is made by an authenticated principal, and its roles are the roles stored for that
principal. Anything else is rejected with 401 (or 403 when the role is insufficient).

## Ways to authenticate

| Path | How | Where roles come from |
|---|---|---|
| **Login credentials** (primary) | `POST /api/v1/auth/login` with `{"username", "password"}`; returns a signed, expiring session token used as `Authorization: Bearer ...` | The user record in the credential store, re-read on every request (role changes and disabling take effect immediately; roles inside the token are ignored) |
| **API token** | `Authorization: Bearer eoip_pat_...` | The token's own role set, always a subset of its principal's roles |
| **ASG file token** | `Authorization: Bearer ...` matching a `sha256:` line in `EOIP_ASG_FILE` | The roles on that line |
| **SSO** (OIDC / SAML 2.0, opt-in) | `GET /api/v1/auth/sso/{oidc,saml}/login` redirects to the IdP; the callback (`GET .../oidc/callback`) or ACS (`POST .../saml/acs`) returns a session token | The provisioned user's stored roles, narrowed to those selected by IdP groups at login; re-read every request (revocations and disabling apply at once, nothing is added) |

Passwords are hashed with argon2id (`argon2-cffi`). API tokens and ASG tokens are stored
only as sha256 digests. The credential store is `<EOIP_DATA_DIR>/state/credentials.json`
(or `EOIP_CREDENTIALS_FILE`), written with mode 0600. Ten failed logins for one username
within five minutes lock that username for the rest of the window. `POST /api/v1/auth/logout`
revokes the presented session token. `GET /api/v1/auth/whoami` shows the effective identity.

Roles: `superadmin` (cross-tenant; implies `admin` and `system`), `admin`, `system`,
`steward`, `analyst`, `viewer`. Every non-superadmin principal is bound to a tenant.

## Provisioning (`eoip-admin`)

The first administrator must be created explicitly. Passwords are read from an
environment variable or a file, never from the command line:

```bash
EOIP_ADMIN_PASSWORD='<long random password>' eoip-admin create-admin --username alice
eoip-admin create-admin --username alice --password-file /run/secrets/admin_password

EOIP_USER_PASSWORD='<password>' eoip-admin add-user --username bob --roles analyst --tenant acme
eoip-admin issue-token --username bob --roles viewer --label ci --output-file bob.token   # file mode 0600
eoip-admin set-roles --username bob --roles viewer
eoip-admin disable --username bob
eoip-admin revoke-token --token-id tok_...
eoip-admin list                                   # usernames and roles only
```

Containers run `eoip-admin from-env` before the API starts. It provisions only what the
operator configured and never prints secrets:

* `EOIP_ADMIN_USERNAME` + `EOIP_ADMIN_PASSWORD` (or `EOIP_ADMIN_PASSWORD_FILE`): create
  that superadmin if it does not exist yet (an existing user is left unchanged; remove
  the password from the environment after the first start).
* `EOIP_API_TOKEN` + `EOIP_API_TOKEN_ROLES` (+ `EOIP_API_TOKEN_PRINCIPAL`,
  `EOIP_API_TOKEN_TENANT`): map the service token used by the MCP facade to its own
  principal with exactly those roles. Without roles the token is not mapped and grants
  nothing.

`scripts/container.sh` / `scripts/container.ps1` generate `deploy/.env` with an admin
username (your login name unless `EOIP_ADMIN_USERNAME` is set), a random admin password and
a service token limited to `analyst`. If no principal exists at all (no ASG entry, empty
credential store) the API refuses to start.

## Single sign-on (OIDC and SAML 2.0)

SSO is **off unless configured**: with `EOIP_SSO_PROVIDER` unset, `GET /api/v1/auth/providers`
lists `oidc` and `saml` as `enabled: false` and `/login` answers 501. An unknown provider name or
an incomplete configuration is a startup error (fail closed). Install with the `sso` extra
(`pip install -e ".[sso]"`; `signxml` for XML-DSig, `httpx` for the OIDC back channel).

| Setting | Meaning |
|---|---|
| `EOIP_SSO_PROVIDER` | `oidc`, `saml` or `oidc,saml` |
| `EOIP_OIDC_ISSUER`, `EOIP_OIDC_CLIENT_ID` | IdP issuer (discovery at `/.well-known/openid-configuration`) and client id |
| `EOIP_OIDC_CLIENT_SECRET_FILE` (or `EOIP_OIDC_CLIENT_SECRET`) | Confidential-client secret (`client_secret_basic`) |
| `EOIP_OIDC_REDIRECT_URI` | Public URL of `/api/v1/auth/sso/oidc/callback` (never derived from the Host header) |
| `EOIP_SAML_SP_ENTITY_ID`, `EOIP_SAML_ACS_URL` | This SP's entity id (the expected Audience) and public `/api/v1/auth/sso/saml/acs` URL |
| `EOIP_SAML_IDP_METADATA_FILE` | IdP metadata XML (entity id, HTTP-Redirect SSO URL, signing certificate) |
| `EOIP_SSO_GROUP_ROLES` | Optional JSON `{"idp-group": ["eoip-role", ...]}` |

What is enforced (`eoip.authn.sso_providers`):

* **OIDC**: authorization code flow with PKCE (S256), `state` and `nonce` (single use, 10-minute
  TTL); issuer must match discovery; ID token signature checked against the IdP JWKS (refetched
  on an unknown `kid`), plus `iss`, `aud`, `azp`, `exp`/`iat` with 30 s leeway and `nonce`.
* **SAML 2.0**: SP-initiated AuthnRequest (HTTP-Redirect), Response via HTTP-POST. The XML
  signature is verified with the configured IdP certificate (`signxml`, exactly one reference) and
  **only the signed element is read**, so injected or wrapped unsigned assertions are ignored
  (XSW). `InResponseTo` must match an outstanding request (single use, so replays and unsolicited
  responses fail), plus Status, Destination, Issuer, Conditions (NotBefore/NotOnOrAfter),
  AudienceRestriction and a bearer SubjectConfirmation addressed to the ACS URL.
* **Mapping**: the IdP username (`preferred_username` / NameID) must be a provisioned, enabled user
  in the credential store (SSO-only users can be created without a password). With
  `EOIP_SSO_GROUP_ROLES`, the session gets the user's stored roles that the IdP groups select;
  if none are selected, sign-in is refused. IdP claims never create a principal or a role.
* Pending logins are held in process memory: run the API as one process or with sticky sessions.

Tested end to end against Keycloak 26 (realm, clients and users created per run; the CI job
`sso-keycloak` in `validation-evidence.yml` runs `tests/security/test_sso_keycloak.py`), including
replay, forged state, wrong client secret, tampered ID token and NameID, signature wrapping,
wrong audience, expiry and a foreign signing certificate. Validation against a customer's own
IdP (Entra ID, Okta, ADFS) is still pending.
