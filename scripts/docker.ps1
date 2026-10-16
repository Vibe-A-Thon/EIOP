<#
.SYNOPSIS
    Docker-specific container orchestration for EOIP (backward-compatible wrapper).
.DESCRIPTION
    This script is retained for backward compatibility. It delegates to the
    universal container.ps1 script, which auto-detects Docker, Podman, nerdctl,
    Finch, or any OCI-compatible runtime.

    For new usage, prefer: scripts/container.ps1

    To force Docker specifically:
        $env:EOIP_CONTAINER_RUNTIME = 'docker'
        scripts/container.ps1 up
#>
param(
    [ValidateSet('up', 'rebuild', 'hubble-local-admin', 'demo-data', 'test', 'status', 'logs', 'down', 'backup', 'backup-bundle', 'extension', 'restore-test', 'acceptance', 'recovery-acceptance', 'dlq-acceptance')]
    [string]$Action = 'up'
)

$containerScript = Join-Path $PSScriptRoot 'container.ps1'
& $containerScript -Action $Action
