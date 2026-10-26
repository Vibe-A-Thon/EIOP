<#
.SYNOPSIS
    One-click PowerShell runner for the KnowGridFlow QA Automation Test Bench.

.PARAMETER Suite
    Test suite to execute: api, selenium, perf, e2e, all (default: api)

.PARAMETER Headless
    Whether to run browser headless (default: true)

.PARAMETER Browser
    Browser type: chrome, edge (default: chrome)

.EXAMPLE
    .\qa_bench\run_qa_bench.ps1 -Suite api
    .\qa_bench\run_qa_bench.ps1 -Suite selenium -Headless $true
    .\qa_bench\run_qa_bench.ps1 -Suite perf
#>
param (
    [ValidateSet("api", "selenium", "playwright", "perf", "e2e", "security", "chaos", "load", "all")]
    [string]$Suite = "api",

    [bool]$Headless = $true,

    [ValidateSet("chrome", "edge")]
    [string]$Browser = "chrome",

    [string]$Filter = "",

    [switch]$VerboseOutput
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RepoRoot = Split-Path -Parent $ScriptDir

$cmd = @(
    "python",
    "$ScriptDir\run_qa_bench.py",
    "--suite", $Suite,
    "--browser", $Browser
)

if ($Headless) {
    $cmd += "--headless"
} else {
    $cmd += "--no-headless"
}

if ($Filter) {
    $cmd += @("-k", $Filter)
}

if ($VerboseOutput) {
    $cmd += "-v"
}

Push-Location $RepoRoot
try {
    & $cmd[0] $cmd[1..($cmd.Length - 1)]
} finally {
    Pop-Location
}
