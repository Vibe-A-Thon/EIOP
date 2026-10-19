# Local Workspace Bootstrap

## Directory Layout

Keep the existing checkout untouched. The workspace parent is **not** a Git repository; each child is its own clone.

```text
F:/code/EIP/
  EIOP/                                  existing legacy checkout
  eopisuite-workspace/                    plain directory, no .git here
    eoip-suite.local.code-workspace       generated local editor configuration
    eoip-suite/.git/
    eoip-engineering/.git/
    eoip-contracts/.git/
    eoip-ui/.git/
    eoip-suite-home/.git/
    eoip-query-portal/.git/
    eoip-knowledge-portal/.git/
    .local/                              ignored/unversioned local secrets and evidence
```

Do not initialize Git in the parent, clone inside `EIOP`, copy `.git`, or create a giant parent commit containing child repositories. No submodules are required. The documents currently live inside the old project as requested; that does not make their directory the future repository parent.

## Prerequisite Checks

Install Git, VS Code with `code` on PATH, GitHub CLI, a reviewed Node 22 toolchain and Python 3.11 baseline environment. Use a supported container runtime for the existing deployment profile when running integrated persistence. Versions must be recorded, not assumed from a successful executable lookup.

```powershell
git --version
gh --version
code --version
node --version
npm --version
py -3.11 --version
gh auth status
```

Choose either native Windows or WSL for a given checkout's dependencies. Do not share a `.venv` or `node_modules` between operating systems. The following bootstrap targets native Windows PowerShell. It does not install tools or alter global Git configuration.

## Clone and Generate the Local Workspace

After guide 03 creates the pilot repositories, materialize this block as `Bootstrap-Workspace.ps1` in a reviewed location or execute it as a reviewed block. It creates local directories/clones and a new workspace file, but never deletes, resets, pulls, switches existing branches, or overwrites an existing workspace file. Empty remote repositories are acceptable at this stage; application commands are not ready until their source/templates have been imported.

```powershell
$ErrorActionPreference = 'Stop'
$Org = 'AvyukthiAI'
$Root = [IO.Path]::GetFullPath('F:\code\EIP\eopisuite-workspace')
$Legacy = [IO.Path]::GetFullPath('F:\code\EIP\EIOP')
$Repos = @('eoip-suite','eoip-engineering','eoip-contracts','eoip-ui',
           'eoip-suite-home','eoip-query-portal','eoip-knowledge-portal')

if ([string]::IsNullOrWhiteSpace($Org) -or $Org -notmatch '^[A-Za-z0-9][A-Za-z0-9-]*$') {
    throw 'Set a valid GitHub organization handle.'
}
foreach ($Tool in @('git','gh','code')) { $null = Get-Command $Tool -ErrorAction Stop }
if (-not (Test-Path -LiteralPath (Join-Path $Legacy '.git'))) {
    throw 'The legacy path must identify the existing checkout.'
}
$Cursor = $Root
while ($Cursor) {
    if (Test-Path -LiteralPath (Join-Path $Cursor '.git')) {
        throw "Workspace parent is inside a Git checkout: $Cursor"
    }
    $Parent = [IO.Directory]::GetParent($Cursor)
    if ($null -eq $Parent) { break }
    $Cursor = $Parent.FullName
}
foreach ($Name in $Repos) {
    gh repo view "$Org/$Name" --json nameWithOwner --jq .nameWithOwner
    if ($LASTEXITCODE -ne 0) { throw "Cannot access $Org/$Name; no local changes made yet." }
}
$null = New-Item -ItemType Directory -Path $Root -Force
foreach ($Name in $Repos) {
    if ($Name -notmatch '^eoip-[a-z0-9-]+$') { throw 'Invalid repository name.' }
    $Destination = [IO.Path]::GetFullPath((Join-Path $Root $Name))
    if ([IO.Directory]::GetParent($Destination).FullName -ne $Root) {
        throw 'Repository destination escaped the workspace parent.'
    }
    if (Test-Path -LiteralPath $Destination) {
        if (-not (Test-Path -LiteralPath (Join-Path $Destination '.git'))) {
            throw "Existing path is not a clone: $Destination"
        }
        $Top = git -C $Destination rev-parse --show-toplevel
        if ($LASTEXITCODE -ne 0 -or [IO.Path]::GetFullPath($Top) -ne $Destination) {
            throw "Unexpected repository root: $Destination"
        }
        $Remote = git -C $Destination remote get-url origin
        if ($LASTEXITCODE -ne 0) { throw "Missing origin: $Destination" }
        $Allowed = @("https://github.com/$Org/$Name.git", "https://github.com/$Org/$Name",
                     "git@github.com:${Org}/${Name}.git")
        if ($Remote -notin $Allowed) { throw "Unexpected origin for $Name; inspect manually." }
        Write-Host "Keeping existing clone and branch: $Name"
    } else {
        git clone "https://github.com/$Org/$Name.git" $Destination
        if ($LASTEXITCODE -ne 0) { throw "Clone failed: $Name. Inspect before retrying." }
    }
}
$Workspace = Join-Path $Root 'eoip-suite.local.code-workspace'
if (Test-Path -LiteralPath $Workspace) {
    Write-Host "Keeping existing workspace: $Workspace"
} else {
    $Folders = @($Repos | ForEach-Object { @{name=$_; path=$_} })
    $Folders += @{name='legacy-eoip'; path=$Legacy.Replace('\','/')}
    $Config = @{
        folders = $Folders
        settings = @{
            'workbench.editor.labelFormat' = 'medium'
            'git.autoRepositoryDetection' = 'subFolders'
            'search.exclude' = @{'**/node_modules'=$true; '**/.venv'=$true; '**/dist'=$true}
            'files.watcherExclude' = @{'**/node_modules/**'=$true; '**/.venv/**'=$true}
        }
        extensions = @{recommendations=@('ms-python.python','ms-python.debugpy')}
    }
    $Json = $Config | ConvertTo-Json -Depth 12
    [IO.File]::WriteAllText($Workspace, $Json, [Text.UTF8Encoding]::new($false))
}
code --reuse-window $Workspace
if ($LASTEXITCODE -ne 0) { throw 'Workspace created; opening VS Code failed.' }
```

The block checks all remote access before creating clones, but it is not an atomic transaction: network failure can leave earlier successful clones in place. A retry preserves existing clones and refuses unexpected paths. Do not solve a failure by recursively deleting the parent directory. No credentials are embedded in remotes or workspace files.

## Development Manifest Versus Release Lock

In `eoip-suite`, implement `repos.json` for repository discovery and profile selection. The following is a **partial schema example**, not the full catalog or a released pin:

```json
{
  "schemaVersion": 1,
  "organization": "AvyukthiAI",
  "repositories": [
    {"name": "eoip-contracts", "defaultBranch": "main", "profiles": ["pilot", "full"]},
    {"name": "eoip-ui", "defaultBranch": "main", "profiles": ["pilot", "full"]},
    {"name": "eoip-query-portal", "defaultBranch": "main", "profiles": ["pilot", "full"]}
  ]
}
```

Populate all selected catalog entries; validate duplicate names, invalid paths, organization mismatch, unrecognized profiles and missing repositories. Do not execute arbitrary command strings from this manifest.

`suite.lock.json` is different: it records exact source commits and artifact digests for a tested combination. The generator must reject unresolved placeholders, moving branches, dirty/uncommitted production inputs and inaccessible artifacts. Developers keep feature branches; a release verifier uses separate clean checkouts at locked commits. Never automatically reset developers' work to a suite lock.

## Add a Repository Later

Create it privately, import its reviewed baseline, grant access and add its manifest entry. Clone it as a sibling. In the current editor use **File > Add Folder to Workspace**, or `code --add` with its absolute path, then retain the workspace changes in the appropriate local/shared file. A full shared workspace can list all cloned repositories; a pilot workspace should not contain nonexistent future folders.

Bootstrap acceptance: each folder has its own Git root and correct remote; Source Control shows independent repositories; cross-root search works; closing/reopening the workspace retains folders; no old code/data was moved; empty repositories are clearly identified as not yet runnable.
