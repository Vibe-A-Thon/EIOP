param(
    [ValidateSet('up', 'test', 'status', 'logs', 'down', 'backup', 'backup-bundle', 'extension', 'restore-test', 'acceptance', 'recovery-acceptance', 'dlq-acceptance')]
    [string]$Action = 'up'
)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$dockerCommand = Get-Command docker -ErrorAction SilentlyContinue
if (-not $dockerCommand) {
    $candidates = @(
        (Join-Path $env:LOCALAPPDATA 'Programs\DockerDesktop\resources\bin\docker.exe'),
        'C:\Program Files\Docker\Docker\resources\bin\docker.exe'
    )
    $dockerPath = $candidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
    if (-not $dockerPath) { throw 'Docker CLI was not found. Install/start Docker Desktop.' }
    $env:Path = "$(Split-Path -Parent $dockerPath);$env:Path"
}
$envFile = Join-Path $projectRoot 'deploy\.env'
if (-not (Test-Path -LiteralPath $envFile)) {
    if ($Action -ne 'up') { throw 'Run scripts/docker.ps1 up once to initialize the local configuration.' }
    $bytes = New-Object byte[] 32
    $random = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    $random.GetBytes($bytes)
    $token = [BitConverter]::ToString($bytes).Replace('-', '').ToLowerInvariant()
    $random.GetBytes($bytes)
    $password = [BitConverter]::ToString($bytes).Replace('-', '').ToLowerInvariant()
    $random.Dispose()
    $config = "EOIP_API_TOKEN=$token`nHUGEGRAPH_PASSWORD=$password`nEOIP_LOAD_DEMO=true`n"
    [System.IO.File]::WriteAllText($envFile, $config, (New-Object System.Text.UTF8Encoding($false)))
    Write-Host 'Created deploy/.env with local credentials. Paste EOIP_API_TOKEN into the web login field.'
}
$composeArguments = @('compose', '--env-file', $envFile, '-f', (Join-Path $projectRoot 'deploy\docker-compose.yml'))
function Invoke-Compose {
    param([string[]]$CommandArguments)
    # Docker writes normal progress to stderr; PowerShell 5.1 must not treat
    # redirected progress as a terminating error. Check the exit code instead.
    $previousErrorPreference = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        & docker @composeArguments @CommandArguments
        $composeExitCode = $LASTEXITCODE
    }
    finally { $ErrorActionPreference = $previousErrorPreference }
    if ($composeExitCode -ne 0) { throw "Docker Compose failed (exit $composeExitCode)." }
}
switch ($Action) {
    'up' { Invoke-Compose -CommandArguments @('up', '--build', '-d', '--wait', '--wait-timeout', '420'); Write-Host 'EOIP: http://localhost:8080/app | API: http://localhost:8000/docs | MCP: http://localhost:8001/mcp' }
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
        $composeArguments = @('compose', '--env-file', $envFile, '-p', $runId, '-f',
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
        $composeArguments = @('compose', '--env-file', $envFile, '-p', $runId, '-f',
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
        $composeArguments = @('compose', '--env-file', $envFile, '-p', $runId, '-f',
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
