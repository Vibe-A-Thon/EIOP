# One VS Code Instance: Workspace, Tasks and Debugging

## Workspace Ownership

The locally generated workspace in guide 04 is usable immediately after cloning. A shared workspace belongs at `eoip-suite/eoip-suite.code-workspace` and uses paths relative to that file. Keep machine-specific legacy paths in the untracked local variant. Use the **same folder aliases** in local and shared workspaces so scoped variables stay valid.

Template for the shared pilot workspace, after all seven pilot repositories exist:

```json
{
  "folders": [
    {"name": "eoip-suite", "path": "."},
    {"name": "eoip-engineering", "path": "../eoip-engineering"},
    {"name": "eoip-contracts", "path": "../eoip-contracts"},
    {"name": "eoip-ui", "path": "../eoip-ui"},
    {"name": "eoip-suite-home", "path": "../eoip-suite-home"},
    {"name": "eoip-query-portal", "path": "../eoip-query-portal"},
    {"name": "eoip-knowledge-portal", "path": "../eoip-knowledge-portal"}
  ],
  "settings": {
    "workbench.editor.labelFormat": "medium",
    "git.autoRepositoryDetection": "subFolders",
    "search.exclude": {"**/node_modules": true, "**/.venv": true, "**/dist": true},
    "files.watcherExclude": {"**/node_modules/**": true, "**/.venv/**": true}
  },
  "extensions": {
    "recommendations": ["ms-python.python", "ms-python.debugpy"]
  }
}
```

VS Code supports folder-specific settings/debuggers alongside shared workspace configuration. Scope workspace variables as `${workspaceFolder:eoip-query-portal}` to avoid using the wrong repository. The editor's Source Control view keeps repositories independent. [Official multi-root guidance](https://code.visualstudio.com/docs/editing/workspaces/multi-root-workspaces).

Trust only reviewed repositories and tasks. Do not enable unrestricted automatic task execution just because all folders belong to one organization. Review extension dependencies and organizational policy before installing additional recommendations.

## Per-Repository Environments

Create a separate `.venv` inside each Python application/library repository and select it through **Python: Select Interpreter** while a file in that folder is active. Pin runtime/dependency versions in that repository. Do not use a global Python environment or a single parent `.venv` to hide missing dependencies.

Install Node dependencies with `npm ci` in the specific repository containing its lockfile. Do not run npm install in the plain parent directory. A shared UI repository can use internal npm workspaces for its own packages; those must not span other Git repositories.

## Query Portal Tasks Template

After the app template supplies actual scripts, place this at `eoip-query-portal/.vscode/tasks.json`. It is not a task file created by this handbook. The explicit Windows executable avoids `.cmd` process-launch ambiguity.

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "query: validate",
      "type": "shell",
      "command": "npm",
      "windows": {"command": "npm.cmd"},
      "args": ["run", "validate"],
      "options": {"cwd": "${workspaceFolder}"},
      "problemMatcher": [],
      "group": "test"
    },
    {
      "label": "query: dev",
      "type": "shell",
      "command": "npm",
      "windows": {"command": "npm.cmd"},
      "args": ["run", "dev", "--", "--host", "127.0.0.1", "--port", "5104", "--strictPort"],
      "options": {"cwd": "${workspaceFolder}"},
      "problemMatcher": [],
      "presentation": {"panel": "dedicated", "reveal": "always"}
    }
  ]
}
```

The dev task is long-running and should be stopped explicitly through VS Code. Do not use it as a sequential prerequisite that must finish before another server starts. A later compound task may start independent servers, but readiness must be determined by real probes; task creation is not a successful startup check.

## Debug Today's Legacy API

In the **local** workspace that includes alias `legacy-eoip`, use the following object as the value of the workspace's `launch` key. It uses existing source, not a nonexistent extracted package. The explicit Python path selects the legacy Windows virtual environment; create/install that environment first. It also requires an ignored `.env.debug` provisioned through the configuration guide. Never commit real secrets in this file.

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Legacy API: isolated memory profile",
      "type": "debugpy",
      "request": "launch",
      "python": "${workspaceFolder:legacy-eoip}/.venv/Scripts/python.exe",
      "module": "uvicorn",
      "args": ["apps.api.main:create_app", "--factory", "--host", "127.0.0.1", "--port", "8000"],
      "cwd": "${workspaceFolder:legacy-eoip}",
      "envFile": "${workspaceFolder:legacy-eoip}/.env.debug",
      "env": {"EOIP_GRAPH_BACKEND": "memory", "EOIP_LOAD_DEMO": "false"},
      "console": "integratedTerminal",
      "justMyCode": true
    }
  ]
}
```

Set a disposable `EOIP_API_TOKEN` of sufficient length and an isolated writable `EOIP_DATA_DIR` privately. Verify `.env.debug` is ignored before creating it. This memory profile is API-only: a separate worker has a different memory graph. Use the existing integrated persistent profile for worker/API journeys. Do not run a host debugger and Compose API on port 8000 simultaneously.

Avoid reload/multiple worker processes when first establishing debugger behavior. After runtime extraction, use folder-local launch files, the new packaged module names in guide 09, and each application's own interpreter. Verify import paths from a clean environment rather than carrying `PYTHONPATH` pointing at the old project. VS Code's Python debugger supports an explicit interpreter through the `python` property; use the appropriate `.venv/bin/python` path for a separately provisioned Linux/WSL environment. [Python debugging configuration](https://code.visualstudio.com/docs/python/debugging).

## Browser and Extension Debugging

Debug the Query portal through the suite gateway once it exists, not only its direct Vite URL. Confirm source maps, routed HMR, secure session behavior and deep links. For early token-mode exploration, use the direct local profile described in guide 07 and mark its limitations.

The existing extension's development host may open another VS Code window; this is the test host required to exercise an extension, not a requirement to maintain separate editor instances for every application. Keep ordinary suite development in the main workspace. Test the extension with two roots, duplicate relative filenames, a non-first active root, denied paths and source links that must not escape the configured repository.

## Common Editor Mistakes

| Symptom | Check |
|---|---|
| Import works in one folder but not tests | Selected interpreter, installed wheel, declared dependencies and package resources |
| Git commit appears in wrong project | Source Control repository selection and terminal working directory |
| Workspace task cannot resolve a path | Folder alias matches scoped variable; path is relative to workspace file location |
| App starts on unexpected port | Add `--strictPort`; inspect conflict rather than silently changing the catalog |
| Search or watcher load is excessive | Open the needed profile; exclude generated dependencies without hiding source from audit |
| AI agent edits a similarly named file elsewhere | State the permitted repositories and exact paths in the task; review each repo diff separately |

One workspace is not one Git transaction and does not guarantee every coding agent or extension reads every root. Explicitly provide repository scope and cross-repository dependencies in each work item.
