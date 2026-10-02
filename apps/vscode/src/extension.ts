import * as vscode from "vscode";

let outputChannel: vscode.OutputChannel;

interface ApiConfig {
  baseUrl: string;
  token: string;
}

function getConfig(): ApiConfig {
  const cfg = vscode.workspace.getConfiguration("eoip");
  return {
    baseUrl: cfg.get<string>("apiUrl", "http://localhost:8000"),
    token: cfg.get<string>("apiToken", ""),
  };
}

async function apiFetch(path: string, options?: RequestInit): Promise<any> {
  const { baseUrl, token } = getConfig();
  const url = `${baseUrl}${path}`;
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  const resp = await fetch(url, { ...options, headers });
  if (!resp.ok) {
    throw new Error(`EOIP API ${resp.status}: ${resp.statusText}`);
  }
  return resp.json();
}

function currentSymbolId(): string | undefined {
  const editor = vscode.window.activeTextEditor;
  if (!editor) return undefined;
  const wsFolder = vscode.workspace.getWorkspaceFolder(editor.document.uri);
  if (!wsFolder) return undefined;
  const relPath = vscode.workspace
    .asRelativePath(editor.document.uri, false)
    .replace(/\\/g, "/");
  const line = editor.selection.active.line + 1;
  return `file:${relPath}:${line}`;
}

export function activate(context: vscode.ExtensionContext) {
  outputChannel = vscode.window.createOutputChannel("EOIP Explorer");

  context.subscriptions.push(
    vscode.commands.registerCommand("eoip.showContext", async () => {
      const editor = vscode.window.activeTextEditor;
      if (!editor) {
        vscode.window.showWarningMessage("No active editor");
        return;
      }
      const wsFolder = vscode.workspace.getWorkspaceFolder(editor.document.uri);
      if (!wsFolder) return;
      const relPath = vscode.workspace
        .asRelativePath(editor.document.uri, false)
        .replace(/\\/g, "/");

      try {
        const result = await apiFetch(
          `/api/v1/search?q=${encodeURIComponent(relPath)}&limit=10`
        );
        const nodes = result.nodes || [];
        if (nodes.length === 0) {
          vscode.window.showInformationMessage(
            `EOIP: No graph entities found for ${relPath}`
          );
          return;
        }
        outputChannel.clear();
        outputChannel.appendLine(`Graph context for: ${relPath}`);
        outputChannel.appendLine("─".repeat(60));
        for (const node of nodes) {
          outputChannel.appendLine(
            `[${node.label}] ${node.id}`
          );
          if (node.properties?.qualified_name) {
            outputChannel.appendLine(
              `  symbol: ${node.properties.qualified_name}`
            );
          }
          if (node.properties?.issue_key) {
            outputChannel.appendLine(
              `  jira: ${node.properties.issue_key}`
            );
          }
        }
        outputChannel.show(true);
      } catch (err: any) {
        vscode.window.showErrorMessage(
          `EOIP: ${err.message || "API unavailable"}`
        );
      }
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand("eoip.traceImpact", async () => {
      const id = await vscode.window.showInputBox({
        prompt: "Canonical ID to trace impact",
        placeHolder: "urn:eoip:work:item:jira:EOIP-1",
      });
      if (!id) return;
      try {
        const result = await apiFetch("/api/v1/agents/trace-impact", {
          method: "POST",
          body: JSON.stringify({ canonical_id: id, max_depth: 4 }),
        });
        outputChannel.clear();
        outputChannel.appendLine(`Impact trace: ${id}`);
        outputChannel.appendLine("─".repeat(60));
        outputChannel.appendLine(`Summary: ${result.summary}`);
        outputChannel.appendLine(`Evidence refs: ${(result.evidence_refs || []).length}`);
        for (const ref of result.evidence_refs || []) {
          outputChannel.appendLine(`  ${ref}`);
        }
        outputChannel.show(true);
      } catch (err: any) {
        vscode.window.showErrorMessage(
          `EOIP: ${err.message || "Trace impact failed"}`
        );
      }
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand("eoip.findPath", async () => {
      const source = await vscode.window.showInputBox({
        prompt: "Source canonical ID",
        placeHolder: "urn:eoip:work:item:jira:EOIP-1",
      });
      if (!source) return;
      const target = await vscode.window.showInputBox({
        prompt: "Target canonical ID",
        placeHolder: "urn:eoip:code:symbol:demo:...",
      });
      if (!target) return;
      try {
        const result = await apiFetch("/api/v1/path", {
          method: "POST",
          body: JSON.stringify({
            source_id: source,
            target_id: target,
            max_depth: 8,
          }),
        });
        outputChannel.clear();
        outputChannel.appendLine(`Path: ${source} → ${target}`);
        outputChannel.appendLine("─".repeat(60));
        const nodes = result.nodes || [];
        const edges = result.edges || [];
        if (nodes.length === 0) {
          outputChannel.appendLine("No path found.");
        } else {
          for (const node of nodes) {
            outputChannel.appendLine(`  [${node.label}] ${node.id}`);
          }
          outputChannel.appendLine(`\nEdge types: ${edges.map((e: any) => e.type).join(" → ")}`);
        }
        outputChannel.show(true);
      } catch (err: any) {
        vscode.window.showErrorMessage(
          `EOIP: ${err.message || "Path query failed"}`
        );
      }
    })
  );

  outputChannel.appendLine("EOIP Explorer activated");
}

export function deactivate() {
  outputChannel?.dispose();
}
