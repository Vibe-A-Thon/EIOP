<#
.SYNOPSIS
    Universal OCI container orchestration for EOIP.
.DESCRIPTION
    Auto-detects Docker, Podman, nerdctl, Finch, or any OCI-compatible
    container runtime and compose tool, then delegates build/deploy/manage
    operations through a single entry point.

    Override auto-detection:
        $env:EOIP_CONTAINER_RUNTIME = 'podman'   # force a specific runtime
        $env:EOIP_COMPOSE_COMMAND   = 'podman-compose'  # force a specific compose

.EXAMPLE
    scripts/container.ps1 up           # build + start (auto-detect runtime)
    scripts/container.ps1 rebuild      # no-cache rebuild
    scripts/container.ps1 status       # container health
    scripts/container.ps1 detect       # print detected runtime info
#>
param(
    [ValidateSet(
        'up', 'rebuild', 'hubble-local-admin', 'demo-data', 'test',
        'status', 'logs', 'down', 'backup', 'backup-bundle', 'extension',
        'restore-test', 'acceptance', 'recovery-acceptance', 'dlq-acceptance',
        'detect', 'info'
    )]
    [string]$Action = 'up'
)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot

# ─── Runtime detection ──────────────────────────────────────────────────
$RuntimeCandidates = @(
    @{ Name = 'docker';       Cli = 'docker';   ComposeProbes = @(@('docker','compose'), @('docker-compose')) }
    @{ Name = 'podman';       Cli = 'podman';   ComposeProbes = @(@('podman','compose'), @('podman-compose')) }
    @{ Name = 'nerdctl';      Cli = 'nerdctl';  ComposeProbes = @(@('nerdctl','compose')) }
    @{ Name = 'finch';        Cli = 'finch';    ComposeProbes = @(@('finch','compose')) }
    @{ Name = 'lima-nerdctl';  Cli = 'lima';     CliArgs = @('nerdctl'); ComposeProbes = @(@('lima','nerdctl','compose')) }
)

function Invoke-CommandVector {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Command,
        [string[]]$Arguments = @()
    )

    if (-not $Command -or $Command.Count -eq 0) {
        throw 'Command vector cannot be empty.'
    }

    $executable = $Command[0]
    $baseArguments = if ($Command.Count -gt 1) { $Command[1..($Command.Count - 1)] } else { @() }
    & $executable @baseArguments @Arguments
}

function Find-ContainerRuntime {
    $override = $env:EOIP_CONTAINER_RUNTIME
    $candidates = $RuntimeCandidates
    if ($override) {
        $norm = $override.ToLower().Replace(' ', '-')
        $candidates = @($candidates | Where-Object { $_.Name -eq $norm }) +
                      @($candidates | Where-Object { $_.Name -ne $norm })
    }

    foreach ($c in $candidates) {
        $cli = $c.Cli
        # Docker Desktop: check standard install paths on Windows
        if ($cli -eq 'docker') {
            $found = Get-Command $cli -ErrorAction SilentlyContinue
            if (-not $found) {
                $winPaths = @(
                    (Join-Path $env:LOCALAPPDATA 'Programs\DockerDesktop\resources\bin\docker.exe'),
                    'C:\Program Files\Docker\Docker\resources\bin\docker.exe'
                )
                $winPath = $winPaths | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
                if ($winPath) { $env:Path = "$(Split-Path -Parent $winPath);$env:Path" }
                else { continue }
            }
        }
        elseif ($cli -eq 'podman') {
            $found = Get-Command $cli -ErrorAction SilentlyContinue
            if (-not $found) {
                $winPaths = @(
                    (Join-Path $env:LOCALAPPDATA 'Programs\RedHat\Podman\podman.exe'),
                    'C:\Program Files\RedHat\Podman\podman.exe'
                )
                $winPath = $winPaths | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
                if ($winPath) { $env:Path = "$(Split-Path -Parent $winPath);$env:Path" }
                else { continue }
            }
        }
        else {
            $found = Get-Command $cli -ErrorAction SilentlyContinue
            if (-not $found) { continue }
        }

        # Verify CLI responds
        $cliArgs = @($cli) + @(if ($c.CliArgs) { $c.CliArgs } else { @() })
        $previousPref = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
        try { $versionOutput = Invoke-CommandVector -Command $cliArgs -Arguments @('--version') 2>$null; $rc = $LASTEXITCODE }
        finally { $ErrorActionPreference = $previousPref }
        if ($rc -ne 0 -or -not $versionOutput) { continue }

        # Probe compose
        $composeCmd = $null
        $composeOverride = $env:EOIP_COMPOSE_COMMAND
        if ($composeOverride) {
            $parts = $composeOverride -split ' '
            $previousPref = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
            try { Invoke-CommandVector -Command $parts -Arguments @('version') 2>$null | Out-Null; $rc = $LASTEXITCODE }
            finally { $ErrorActionPreference = $previousPref }
            if ($rc -eq 0) { $composeCmd = $parts }
        }
        if (-not $composeCmd) {
            foreach ($probe in $c.ComposeProbes) {
                $previousPref = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
                try { Invoke-CommandVector -Command $probe -Arguments @('version') 2>$null | Out-Null; $rc = $LASTEXITCODE }
                finally { $ErrorActionPreference = $previousPref }
                if ($rc -eq 0) { $composeCmd = $probe; break }
            }
        }

        return @{
            Name           = $c.Name
            Cli            = $cliArgs
            Version        = ($versionOutput -join ' ').Trim()
            ComposeCmd     = $composeCmd
            ComposeVersion = if ($composeCmd) {
                $previousPref = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
                try { $cv = Invoke-CommandVector -Command $composeCmd -Arguments @('version') 2>$null; ($cv -join ' ').Trim() }
                finally { $ErrorActionPreference = $previousPref }
            } else { $null }
        }
    }
    return $null
}

$Runtime = Find-ContainerRuntime
if (-not $Runtime) {
    throw @"
No OCI container runtime found on this system.
Install one of: Docker, Podman, nerdctl, or Finch.
Override detection with: `$env:EOIP_CONTAINER_RUNTIME = '<name>'
"@
}

$rt = $Runtime.Name
$cliCmd = $Runtime.Cli
$composeCmd = $Runtime.ComposeCmd

Write-Host "EOIP Container Runtime: $rt ($($Runtime.Version))" -ForegroundColor Cyan
if ($composeCmd) {
    Write-Host "  Compose: $($composeCmd -join ' ') ($($Runtime.ComposeVersion))" -ForegroundColor DarkCyan
}

if ($Action -eq 'detect' -or $Action -eq 'info') {
    Write-Host ''
    Write-Host "Runtime:          $rt"
    Write-Host "CLI:              $($cliCmd -join ' ')"
    Write-Host "Version:          $($Runtime.Version)"
    Write-Host "Compose:          $(if ($composeCmd) { $composeCmd -join ' ' } else { '(none)' })"
    Write-Host "Compose Version:  $(if ($Runtime.ComposeVersion) { $Runtime.ComposeVersion } else { 'N/A' })"

    # Probe for other available runtimes
    Write-Host ''
    Write-Host 'All detected runtimes:' -ForegroundColor Yellow
    foreach ($c in $RuntimeCandidates) {
        $cli = $c.Cli
        $found = Get-Command $cli -ErrorAction SilentlyContinue
        $status = if ($found) { 'available' } else { 'not found' }
        $marker = if ($c.Name -eq $rt) { ' (active)' } else { '' }
        Write-Host "  $($c.Name): $status$marker"
    }
    exit 0
}

if (-not $composeCmd) {
    throw "Compose tool not found for runtime '$rt'. Install ${rt} compose plugin or a standalone compose tool."
}

function New-RandomHex {
    param([int]$ByteCount)
    $bytes = New-Object byte[] $ByteCount
    $random = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    try { $random.GetBytes($bytes) } finally { $random.Dispose() }
    return [BitConverter]::ToString($bytes).Replace('-', '').ToLowerInvariant()
}

# ─── Environment / .env ─────────────────────────────────────────────────
$envFile = Join-Path $projectRoot 'deploy\.env'
if (-not (Test-Path -LiteralPath $envFile)) {
    if ($Action -ne 'up') {
        throw "Run scripts/container.ps1 up once to initialize the local configuration."
    }
    $token = New-RandomHex -ByteCount 32     # 64 hex chars (256-bit API token)
    # FT-X04: Hubble stores the graph password in VARCHAR(48) -> 24 bytes = 48 hex chars (192-bit).
    $password = New-RandomHex -ByteCount 24
    $config = "EOIP_API_TOKEN=$token`nHUGEGRAPH_PASSWORD=$password`nEOIP_LOAD_DEMO=true`n"
    [System.IO.File]::WriteAllText($envFile, $config, (New-Object System.Text.UTF8Encoding($false)))
    Write-Host 'Created deploy/.env with local credentials. Paste EOIP_API_TOKEN into the web login field.'
}

# ─── Compose wiring ─────────────────────────────────────────────────────
# Determine the Dockerfile / Containerfile to use
$dockerfile = 'deploy/Dockerfile'
$containerfile = 'deploy/Containerfile'
if ((Test-Path (Join-Path $projectRoot $containerfile)) -and ($rt -ne 'docker')) {
    $dockerfile = $containerfile
}

$composeFile = Join-Path $projectRoot 'deploy\docker-compose.yml'
$composeArguments = @('--env-file', $envFile, '-f', $composeFile)

# Podman compose may need the project name explicitly
if ($rt -eq 'podman') {
    $composeArguments = @('-p', 'eoip') + $composeArguments
}

function Invoke-Compose {
    param([string[]]$CommandArguments)
    $previousErrorPreference = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        Invoke-CommandVector -Command $composeCmd -Arguments (@($composeArguments) + @($CommandArguments))
        $composeExitCode = $LASTEXITCODE
    }
    finally { $ErrorActionPreference = $previousErrorPreference }
    if ($composeExitCode -ne 0) {
        throw "$($composeCmd -join ' ') compose failed (exit $composeExitCode)."
    }
}

function Invoke-Runtime {
    param([string[]]$CommandArguments)
    $previousErrorPreference = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        Invoke-CommandVector -Command $cliCmd -Arguments @($CommandArguments)
        $rtExitCode = $LASTEXITCODE
    }
    finally { $ErrorActionPreference = $previousErrorPreference }
    if ($rtExitCode -ne 0) {
        throw "$($cliCmd -join ' ') failed (exit $rtExitCode)."
    }
}

# ─── Actions ─────────────────────────────────────────────────────────────
switch ($Action) {
    'up' {
        Invoke-Compose -CommandArguments @('up', '--build', '-d', '--wait', '--wait-timeout', '420')
        Write-Host "EOIP ($rt): http://localhost:8080/app | API: http://localhost:8000/docs | MCP: http://localhost:8001/mcp | Hubble: http://localhost:8088"
    }
    'rebuild' {
        Invoke-Compose -CommandArguments @('build', '--no-cache', 'eoip-api', 'eoip-web', 'hubble')
        Invoke-Compose -CommandArguments @('up', '-d', '--force-recreate', '--wait', '--wait-timeout', '420')
        Write-Host "Clean rebuild complete ($rt). Existing graph, application, model and Hubble volumes were retained."
    }
    'hubble-local-admin' {
        if ($env:HUGEGRAPH_PASSWORD) { throw 'Unset the process HUGEGRAPH_PASSWORD override before rotating the local account.' }
        $config = [System.IO.File]::ReadAllText($envFile)
        if ([regex]::Matches($config, '(?m)^HUGEGRAPH_PASSWORD=[^\r\n]*').Count -ne 1) {
            throw 'deploy/.env must contain exactly one HUGEGRAPH_PASSWORD entry.'
        }
        # FT-SEC-HUBBLE: rotate to a fresh random password (never admin/admin). The value is
        # passed by environment-variable NAME only (not on the command line) and never printed.
        $newPassword = New-RandomHex -ByteCount 24
        Invoke-Compose -CommandArguments @('build', 'schema-init', 'hubble')
        $env:EOIP_HUGEGRAPH_NEW_PASSWORD = $newPassword
        try {
            Invoke-Compose -CommandArguments @('run', '--rm', '--no-deps', '-e', 'EOIP_HUGEGRAPH_NEW_PASSWORD', 'schema-init',
                'python', '-m', 'scripts.setup_hubble', '--rotate-local-admin')
        }
        finally { Remove-Item Env:EOIP_HUGEGRAPH_NEW_PASSWORD -ErrorAction SilentlyContinue }
        $config = [regex]::Replace($config, '(?m)^HUGEGRAPH_PASSWORD=[^\r\n]*', "HUGEGRAPH_PASSWORD=$newPassword")
        [System.IO.File]::WriteAllText($envFile, $config, (New-Object System.Text.UTF8Encoding($false)))
        Invoke-Compose -CommandArguments @('up', '-d', '--force-recreate', '--wait', '--wait-timeout', '420')
        Write-Host 'Graph admin password rotated to a new random value and saved in deploy/.env (HUGEGRAPH_PASSWORD; not printed). Hubble: http://localhost:8088.'
    }
    'demo-data' {
        Invoke-Compose -CommandArguments @('up', '--build', '-d', '--wait', '--wait-timeout', '420')
        Invoke-Compose -CommandArguments @('exec', '-T', 'eoip-api', 'python', '-m', 'scripts.load_demo_corpus')
        Write-Host 'Demo corpus loaded into the existing graph. Hubble: http://localhost:8088.'
    }
    'test' {
        Invoke-Compose -CommandArguments @('--profile', 'test', 'build', 'tests', 'smoke', 'ui-tests')
        Invoke-Compose -CommandArguments @('--profile', 'test', 'run', '--rm', '--no-deps', 'tests')
        Invoke-Compose -CommandArguments @('--profile', 'test', 'run', '--rm', '--no-deps', 'smoke')
        Invoke-Compose -CommandArguments @('--profile', 'test', 'run', '--rm', '--no-deps', 'ui-tests')
    }
    'status' { Invoke-Compose -CommandArguments @('ps') }
    'logs' { Invoke-Compose -CommandArguments @('logs', '--tail', '100') }
    'down' { Invoke-Compose -CommandArguments @('down') }
    'backup' {
        Invoke-Compose -CommandArguments @('stop', 'eoip-worker')
        try { Invoke-Compose -CommandArguments @('exec', '-T', 'eoip-api', 'python', '-m', 'scripts.backup') }
        finally { Invoke-Compose -CommandArguments @('start', 'eoip-worker') }
    }
    'backup-bundle' {
        $writers = @(@(Invoke-Compose -CommandArguments @('ps', '--status', 'running', '--services')) |
            Where-Object { $_ -in @('eoip-worker', 'eoip-api', 'eoip-mcp', 'local-model') })
        try {
            if ($writers.Count -gt 0) { Invoke-Compose -CommandArguments (@('stop') + $writers) }
            Invoke-Compose -CommandArguments @('--profile', 'tools', 'run', '--rm', '--no-deps', 'bundle-backup')
        }
        finally {
            if ($writers.Count -gt 0) { Invoke-Compose -CommandArguments (@('start') + $writers) }
        }
    }
    'extension' { Invoke-Compose -CommandArguments @('--profile', 'tools', 'run', '--build', '--rm', 'extension-build') }
    'acceptance' {
        $previousAcceptanceRun = $env:EOIP_ACCEPTANCE_RUN
        $runId = "eoip-acceptance-$([Guid]::NewGuid().ToString('N'))"
        $env:EOIP_ACCEPTANCE_RUN = $runId
        $composeArguments = @('--env-file', $envFile, '-p', $runId, '-f',
            (Join-Path $projectRoot 'deploy\docker-compose.acceptance.yml'))
        try {
            Invoke-Compose -CommandArguments @('build', 'acceptance')
            Invoke-Compose -CommandArguments @('up', '--abort-on-container-exit', '--exit-code-from', 'acceptance')
            Write-Host "Acceptance evidence: test-results\$runId.json"
        }
        finally {
            try { Invoke-Compose -CommandArguments @('down', '--volumes') }
            finally { $env:EOIP_ACCEPTANCE_RUN = $previousAcceptanceRun }
        }
    }
    'dlq-acceptance' {
        $previousAcceptanceRun = $env:EOIP_ACCEPTANCE_RUN
        $runId = "eoip-dlq-acceptance-$([Guid]::NewGuid().ToString('N'))"
        $env:EOIP_ACCEPTANCE_RUN = $runId
        $composeArguments = @('--env-file', $envFile, '-p', $runId, '-f',
            (Join-Path $projectRoot 'deploy\docker-compose.dlq-acceptance.yml'))
        try {
            Invoke-Compose -CommandArguments @('build', 'dlq-api', 'acceptance')
            Invoke-Compose -CommandArguments @('up', '-d', '--wait', '--wait-timeout', '420',
                'dlq-api', 'dlq-worker', 'dlq-upstream', 'dlq-confluence')
            Invoke-Compose -CommandArguments @('run', '--rm', '--no-deps', 'acceptance')
            Write-Host "DLQ acceptance evidence: test-results\$runId.json"
        }
        finally {
            try {
                Invoke-Compose -CommandArguments @('logs', '--tail', '80', 'schema-init', 'dlq-api', 'dlq-worker', 'dlq-upstream', 'dlq-confluence')
            }
            finally {
                try { Invoke-Compose -CommandArguments @('down', '--volumes') }
                finally { $env:EOIP_ACCEPTANCE_RUN = $previousAcceptanceRun }
            }
        }
    }
    'recovery-acceptance' {
        $previousAcceptanceRun = $env:EOIP_ACCEPTANCE_RUN
        $runId = "eoip-recovery-acceptance-$([Guid]::NewGuid().ToString('N'))"
        $env:EOIP_ACCEPTANCE_RUN = $runId
        $composeArguments = @('--env-file', $envFile, '-p', $runId, '-f',
            (Join-Path $projectRoot 'deploy\docker-compose.acceptance.yml'))
        try {
            Invoke-Compose -CommandArguments @('build', 'recovery-acceptance')
            Invoke-Compose -CommandArguments @('up', '-d', '--wait', '--wait-timeout', '420',
                'source-graph', 'target-graph')
            Invoke-Compose -CommandArguments @('run', '--rm', '--no-deps', 'recovery-acceptance')
            Write-Host "Recovery evidence: test-results\$runId.json"
        }
        finally {
            try { Invoke-Compose -CommandArguments @('down', '--volumes') }
            finally { $env:EOIP_ACCEPTANCE_RUN = $previousAcceptanceRun }
        }
    }
    'restore-test' {
        try {
            Invoke-Compose -CommandArguments @('--profile', 'restore-test', 'run', '--rm', 'restore-check')
        }
        finally {
            Invoke-Compose -CommandArguments @('--profile', 'restore-test', 'rm', '--stop', '--force', 'restore-graph')
        }
    }
}
