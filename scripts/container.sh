#!/usr/bin/env bash
# Universal OCI container orchestration for EOIP (Linux / macOS).
#
# Auto-detects Docker, Podman, nerdctl, Finch, or any OCI-compatible
# container runtime and compose tool.
#
# Override auto-detection:
#   EOIP_CONTAINER_RUNTIME=podman ./scripts/container.sh up
#   EOIP_COMPOSE_COMMAND="podman-compose" ./scripts/container.sh up
#
# Usage: scripts/container.sh <action>
#   up | rebuild | demo-data | test | status | logs | down | detect | …

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ACTION="${1:-up}"

# ─── Runtime detection ──────────────────────────────────────────────────

RUNTIME_NAME=""
CLI_CMD=""
COMPOSE_CMD=""

detect_runtime() {
    local candidates=("docker" "podman" "nerdctl" "finch")
    local override="${EOIP_CONTAINER_RUNTIME:-}"

    if [ -n "$override" ]; then
        candidates=("$override" "${candidates[@]}")
    fi

    for rt in "${candidates[@]}"; do
        if command -v "$rt" &>/dev/null; then
            if "$rt" --version &>/dev/null; then
                RUNTIME_NAME="$rt"
                CLI_CMD="$rt"
                break
            fi
        fi
    done

    if [ -z "$RUNTIME_NAME" ]; then
        echo "ERROR: No OCI container runtime found." >&2
        echo "Install one of: Docker, Podman, nerdctl, or Finch." >&2
        echo "Override detection with: EOIP_CONTAINER_RUNTIME=<name>" >&2
        exit 1
    fi
}

detect_compose() {
    local override="${EOIP_COMPOSE_COMMAND:-}"
    if [ -n "$override" ]; then
        if $override version &>/dev/null; then
            COMPOSE_CMD="$override"
            return
        fi
    fi

    local probes=()
    case "$RUNTIME_NAME" in
        docker)  probes=("docker compose" "docker-compose") ;;
        podman)  probes=("podman compose" "podman-compose") ;;
        nerdctl) probes=("nerdctl compose") ;;
        finch)   probes=("finch compose") ;;
        *)       probes=("$RUNTIME_NAME compose") ;;
    esac

    for probe in "${probes[@]}"; do
        if $probe version &>/dev/null; then
            COMPOSE_CMD="$probe"
            return
        fi
    done

    echo "ERROR: No compose tool found for runtime '$RUNTIME_NAME'." >&2
    echo "Install ${RUNTIME_NAME} compose plugin or a standalone compose." >&2
    exit 1
}

detect_runtime
detect_compose

echo "EOIP Container Runtime: $RUNTIME_NAME ($($CLI_CMD --version 2>/dev/null | head -1))"
echo "  Compose: $COMPOSE_CMD ($($COMPOSE_CMD version 2>/dev/null | head -1))"

# ─── detect / info action ───────────────────────────────────────────────

if [ "$ACTION" = "detect" ] || [ "$ACTION" = "info" ]; then
    echo ""
    echo "All detected runtimes:"
    for rt in docker podman nerdctl finch; do
        if command -v "$rt" &>/dev/null; then
            marker=""
            [ "$rt" = "$RUNTIME_NAME" ] && marker=" (active)"
            echo "  $rt: available${marker}"
        else
            echo "  $rt: not found"
        fi
    done
    exit 0
fi

# ─── Environment / .env ─────────────────────────────────────────────────

ENV_FILE="$PROJECT_ROOT/deploy/.env"

if [ ! -f "$ENV_FILE" ]; then
    if [ "$ACTION" != "up" ]; then
        echo "ERROR: Run scripts/container.sh up once to initialize configuration." >&2
        exit 1
    fi
    TOKEN=$(openssl rand -hex 32)
    PASSWORD=$(openssl rand -hex 24)  # FT-X04: Hubble VARCHAR(48) -> 48 hex chars, 192-bit
    printf "EOIP_API_TOKEN=%s\nHUGEGRAPH_PASSWORD=%s\nEOIP_LOAD_DEMO=true\n" "$TOKEN" "$PASSWORD" > "$ENV_FILE"
    echo "Created deploy/.env with local credentials. Paste EOIP_API_TOKEN into the web login field."
fi

# ─── Compose wiring ─────────────────────────────────────────────────────

COMPOSE_FILE="$PROJECT_ROOT/deploy/docker-compose.yml"
COMPOSE_BASE_ARGS="--env-file $ENV_FILE -f $COMPOSE_FILE"

# Podman may need explicit project name
if [ "$RUNTIME_NAME" = "podman" ]; then
    COMPOSE_BASE_ARGS="-p eoip $COMPOSE_BASE_ARGS"
fi

run_compose() {
    $COMPOSE_CMD $COMPOSE_BASE_ARGS "$@"
}

# ─── Actions ─────────────────────────────────────────────────────────────

case "$ACTION" in
    up)
        run_compose up --build -d --wait --wait-timeout 420
        echo "EOIP ($RUNTIME_NAME): http://localhost:8080/app | API: http://localhost:8000/docs | MCP: http://localhost:8001/mcp | Hubble: http://localhost:8088"
        ;;
    rebuild)
        run_compose build --no-cache eoip-api eoip-web hubble
        run_compose up -d --force-recreate --wait --wait-timeout 420
        echo "Clean rebuild complete ($RUNTIME_NAME). Existing volumes were retained."
        ;;
    demo-data)
        run_compose up --build -d --wait --wait-timeout 420
        run_compose exec -T eoip-api python -m scripts.load_demo_corpus
        echo "Demo corpus loaded. Hubble: http://localhost:8088."
        ;;
    test)
        run_compose --profile test build tests smoke ui-tests
        run_compose --profile test run --rm --no-deps tests
        run_compose --profile test run --rm --no-deps smoke
        run_compose --profile test run --rm --no-deps ui-tests
        ;;
    status) run_compose ps ;;
    logs)   run_compose logs --tail 100 ;;
    down)   run_compose down ;;
    backup)
        run_compose stop eoip-worker
        run_compose exec -T eoip-api python -m scripts.backup || true
        run_compose start eoip-worker
        ;;
    backup-bundle)
        WRITERS=$(run_compose ps --status running --services 2>/dev/null | grep -E '^(eoip-worker|eoip-api|eoip-mcp|local-model)$' || true)
        if [ -n "$WRITERS" ]; then run_compose stop $WRITERS; fi
        run_compose --profile tools run --rm --no-deps bundle-backup
        if [ -n "$WRITERS" ]; then run_compose start $WRITERS; fi
        ;;
    extension)
        run_compose --profile tools run --build --rm extension-build
        ;;
    acceptance)
        RUN_ID="eoip-acceptance-$(uuidgen 2>/dev/null || python3 -c 'import uuid; print(uuid.uuid4().hex)')"
        export EOIP_ACCEPTANCE_RUN="$RUN_ID"
        COMPOSE_BASE_ARGS="--env-file $ENV_FILE -p $RUN_ID -f $PROJECT_ROOT/deploy/docker-compose.acceptance.yml"
        run_compose build acceptance
        run_compose up --abort-on-container-exit --exit-code-from acceptance || true
        echo "Acceptance evidence: test-results/$RUN_ID.json"
        run_compose down --volumes
        ;;
    recovery-acceptance)
        RUN_ID="eoip-recovery-$(uuidgen 2>/dev/null || python3 -c 'import uuid; print(uuid.uuid4().hex)')"
        export EOIP_ACCEPTANCE_RUN="$RUN_ID"
        COMPOSE_BASE_ARGS="--env-file $ENV_FILE -p $RUN_ID -f $PROJECT_ROOT/deploy/docker-compose.acceptance.yml"
        run_compose build recovery-acceptance
        run_compose up -d --wait --wait-timeout 420 source-graph target-graph
        run_compose run --rm --no-deps recovery-acceptance || true
        echo "Recovery evidence: test-results/$RUN_ID.json"
        run_compose down --volumes
        ;;
    dlq-acceptance)
        RUN_ID="eoip-dlq-$(uuidgen 2>/dev/null || python3 -c 'import uuid; print(uuid.uuid4().hex)')"
        export EOIP_ACCEPTANCE_RUN="$RUN_ID"
        COMPOSE_BASE_ARGS="--env-file $ENV_FILE -p $RUN_ID -f $PROJECT_ROOT/deploy/docker-compose.dlq-acceptance.yml"
        run_compose build dlq-api acceptance
        run_compose up -d --wait --wait-timeout 420 dlq-api dlq-worker dlq-upstream dlq-confluence
        run_compose run --rm --no-deps acceptance || true
        echo "DLQ acceptance evidence: test-results/$RUN_ID.json"
        run_compose logs --tail 80 schema-init dlq-api dlq-worker dlq-upstream dlq-confluence
        run_compose down --volumes
        ;;
    restore-test)
        run_compose --profile restore-test run --rm restore-check || true
        run_compose --profile restore-test rm --stop --force restore-graph
        ;;
    *)
        echo "Unknown action: $ACTION" >&2
        echo "Valid actions: up rebuild demo-data test status logs down detect backup backup-bundle extension acceptance recovery-acceptance dlq-acceptance restore-test" >&2
        exit 1
        ;;
esac
