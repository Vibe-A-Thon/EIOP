#!/usr/bin/env bash
# FT-X03 / FT-F04: build the runtime image and prove the API becomes ready.
# Usage: scripts/ci/container_smoke.sh [runtime-cli]   (default: docker)
# FT-AUTH: there is no default account; the first admin is provisioned from env by the
# image entrypoint ('eoip-admin from-env'). Credentials are generated per run and never
# printed or put on a command line. The in-memory graph backend
# keeps the smoke independent of HugeGraph (covered by the compose acceptance flows).
set -euo pipefail
CLI="${1:-docker}"
IMAGE="${EOIP_SMOKE_IMAGE:-eoip-ci:runtime}"
NAME="eoip-ci-smoke-$$"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

"$CLI" build -f "$ROOT/deploy/Dockerfile" --target runtime -t "$IMAGE" "$ROOT"

ADMIN_PASSWORD="$(python3 -c 'import secrets; print(secrets.token_urlsafe(24))')"
cleanup() { "$CLI" rm -f "$NAME" >/dev/null 2>&1 || true; }
trap cleanup EXIT
# Pass secrets by variable name so they never appear on a command line.
EOIP_ADMIN_USERNAME=ci-admin EOIP_ADMIN_PASSWORD="$ADMIN_PASSWORD" "$CLI" run -d --name "$NAME" -p 127.0.0.1::8000 \
  -e EOIP_ADMIN_USERNAME -e EOIP_ADMIN_PASSWORD -e EOIP_ENV=ci -e EOIP_GRAPH_BACKEND=memory "$IMAGE" >/dev/null
PORT="$("$CLI" port "$NAME" 8000/tcp | head -n1 | sed 's/.*://')"

for _ in $(seq 1 90); do
  if curl -fsS "http://127.0.0.1:$PORT/health/ready" >/dev/null 2>&1; then
    echo "runtime image ready on /health/ready"
    anon="$(curl -s -o /dev/null -w '%{http_code}' "http://127.0.0.1:$PORT/api/v1/admin/jobs")"
    echo "unauthenticated /api/v1/admin/jobs: $anon (expect 401)"
    [[ "$anon" == "401" ]]
    login() {  # JSON body on stdin, so the password is not in argv
      python3 -c 'import json,os,sys; print(json.dumps({"username": sys.argv[1], "password": os.environ["P"]}))' "$1" | \
        curl -s -o "$2" -w '%{http_code}' -H 'Content-Type: application/json' --data-binary @- \
        "http://127.0.0.1:$PORT/api/v1/auth/login"
    }
    bad="$(P=wrong-password-for-smoke login ci-admin /dev/null)"
    echo "login with a wrong password: $bad (expect 401)"
    [[ "$bad" == "401" ]]
    BODY="$(mktemp)"
    ok="$(P="$ADMIN_PASSWORD" login ci-admin "$BODY")"
    echo "login as the provisioned admin: $ok (expect 200)"
    [[ "$ok" == "200" ]]
    SESSION="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["token"])' "$BODY")"; rm -f "$BODY"
    # Header via curl config on stdin, so the session token is not in argv.
    authed="$(printf 'header = "Authorization: Bearer %s"\n' "$SESSION" | \
      curl -s -K - -o /dev/null -w '%{http_code}' "http://127.0.0.1:$PORT/api/v1/admin/jobs")"
    echo "authenticated /api/v1/admin/jobs: $authed (expect 200)"
    [[ "$authed" == "200" ]]
    # The test suite must not ship in the runtime image.
    if "$CLI" exec "$NAME" test -e /opt/eoip/tests; then echo "tests/ present in runtime image" >&2; exit 1; fi
    exit 0
  fi
  if [[ "$("$CLI" inspect -f '{{.State.Running}}' "$NAME")" != "true" ]]; then break; fi
  sleep 2
done
echo "runtime image did not become ready" >&2
"$CLI" logs --tail 80 "$NAME" >&2 || true
exit 1
