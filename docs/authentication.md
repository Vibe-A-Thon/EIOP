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
| SSO (OIDC / SAML) | **Placeholder, not implemented** | -- |

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

## SSO placeholder

`eoip.authn.sso` defines the `SSOProvider` interface (`begin_login`, `complete_login`) and
two **disabled** stubs, `OIDCProviderStub` and `SAMLProviderStub`. `GET
/api/v1/auth/providers` lists them as `enabled: false, status: placeholder`;
`GET /api/v1/auth/sso/{oidc|saml}/login` answers 501; setting `EOIP_SSO_PROVIDER` is a
startup error. A real provider must validate the IdP response (signature, issuer,
audience, nonce, expiry) and map the IdP subject to an explicitly provisioned principal;
IdP claims must never create a principal or role on their own.
