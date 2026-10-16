$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
try {
    Write-Host 'Preparing the real persistent graph and additive enterprise demo corpus...'
    & (Join-Path $root 'scripts\docker.ps1') demo-data
    $response = Invoke-WebRequest 'http://localhost:8088/enterprise.html' -UseBasicParsing
    if ($response.StatusCode -ne 200 -or $response.Content -notmatch 'EOIP Enterprise Graph') {
        throw 'Guided Hubble page is not available.'
    }
    Write-Host 'Opening 11 live graph scenarios, with 15 seconds to inspect each one.'
    Write-Host 'Use Stop walkthrough to inspect names, arrows, domain colors and source evidence.'
    Write-Host 'This demonstrates connected synthetic data, not every production acceptance criterion.'
    Start-Process 'http://localhost:8088/enterprise.html?tour=1'
}
catch {
    Write-Error $_
    exit 1
}
