const vscode = require('vscode');
const http = require('node:http');
const https = require('node:https');
const fs = require('node:fs/promises');
const path = require('node:path');

function codedError(code, message, cause) {
  const error = new Error(message, cause ? {cause} : undefined);
  error.code = code;
  return error;
}

function normalizedPath(value) {
  return typeof value === 'string' ? value.replace(/\\/g, '/').replace(/^\.\/+/, '') : '';
}

function isWithin(root, target) {
  const relative = path.relative(root, target);
  return relative !== '' && relative !== '..' &&
    !relative.startsWith(`..${path.sep}`) && !path.isAbsolute(relative);
}

function repositoryRoot(configuredRoot, workspacePath, filePath) {
  const base = workspacePath || (filePath ? path.dirname(filePath) : process.cwd());
  return path.resolve(base, configuredRoot || workspacePath || path.dirname(filePath || base));
}

function nodeName(node) {
  const properties = node.properties || {};
  return properties.qualified_name || properties.name || properties.summary ||
    properties.title || properties.path || node.label || node.id;
}

function findEnclosingSymbol(symbols, position) {
  let best;
  for (const candidate of symbols) {
    const range = candidate.selectionRange || candidate.range;
    if (!range || !range.contains(position)) continue;
    const child = findEnclosingSymbol(candidate.children || [], position);
    if (child) return child;
    best = candidate.name;
  }
  return best;
}

class ContextProvider {
  constructor(call) {
    this.call = call;
    this.emitter = new vscode.EventEmitter();
    this.onDidChangeTreeData = this.emitter.event;
    this.roots = [
      this.item('Open a source file and run EOIP: Context for Active File.', vscode.TreeItemCollapsibleState.None),
    ];
    this.node = undefined;
    this.relativePath = '';
    this.error = undefined;
    this.relatedCount = 0;
    this.evidenceCount = 0;
  }

  getTreeItem(item) {
    return item;
  }

  getChildren(item) {
    return item ? (item.children || []) : this.roots;
  }

  item(label, state = vscode.TreeItemCollapsibleState.None, description, tooltip) {
    const treeItem = new vscode.TreeItem(label, state);
    if (description) treeItem.description = description;
    if (tooltip) treeItem.tooltip = tooltip;
    return treeItem;
  }

  currentNode() {
    return this.node;
  }

  containsPosition(editor) {
    if (!this.node || !this.relativePath || !editor) return false;
    const sourcePath = normalizedPath(this.node.properties?.path);
    if (sourcePath !== this.relativePath) return false;
    const line = editor.selection.active.line + 1;
    const start = Number(this.node.properties.start_line);
    const end = Number(this.node.properties.end_line || start);
    return Number.isInteger(start) && Number.isInteger(end) && line >= start && line <= end;
  }

  async refresh(editor = vscode.window.activeTextEditor) {
    if (!editor) {
      this.error = codedError('EOIP_NO_ACTIVE_EDITOR', 'Open a source file before refreshing EOIP context.');
      this.setStatus(this.error.message);
      return {ok: false, code: this.error.code, message: this.error.message};
    }

    try {
      const location = await this.locationFor(editor);
      this.relativePath = normalizedPath(location.relativePath);
      this.roots = [this.item('Loading EOIP context…', vscode.TreeItemCollapsibleState.None)];
      this.emitter.fire();
      const query = location.symbol || location.relativePath;
      const search = await this.call(
        `/api/v1/search?q=${encodeURIComponent(query)}&label=CodeSymbol&limit=50`,
      );
      const node = this.findNode(search.nodes || [], location);
      if (!node) {
        throw codedError(
          'EOIP_SYMBOL_NOT_FOUND',
          `No indexed code symbol matched ${location.symbol ? `"${location.symbol}" in ` : ''}${location.relativePath}.`,
        );
      }

      const [impact, lineage] = await Promise.all([
        this.call('/api/v1/impact', {
          canonical_id: node.id,
          max_depth: 4,
          result_limit: 100,
        }),
        this.call('/api/v1/lineage', {
          canonical_id: node.id,
          max_depth: 3,
          result_limit: 50,
        }),
      ]);
      this.node = node;
      this.error = undefined;
      this.roots = this.contextTree(node, location.relativePath, impact, lineage);
      this.emitter.fire();
      return {
        ok: true,
        node,
        relatedCount: this.relatedCount,
        evidenceCount: this.evidenceCount,
      };
    } catch (error) {
      this.error = error.code ? error : codedError('EOIP_CONTEXT_FAILED', error.message || 'Unable to load EOIP context.', error);
      this.setStatus(`${this.error.message}${this.node ? ' — showing the last retrieved context below.' : ''}`, Boolean(this.node));
      return {ok: false, code: this.error.code, message: this.error.message};
    }
  }

  async locationFor(editor) {
    const fileName = editor.document.uri.fsPath;
    const configuredRoot = vscode.workspace.getConfiguration('eoip').get('repositoryRoot', '');
    const workspace = vscode.workspace.getWorkspaceFolder(editor.document.uri);
    let root;
    let source;
    try {
      root = await fs.realpath(repositoryRoot(configuredRoot, workspace?.uri.fsPath, fileName));
      source = await fs.realpath(fileName);
    } catch (error) {
      throw codedError('EOIP_SOURCE_NOT_FOUND', 'The active source file or repository root is unavailable.', error);
    }
    const relative = path.relative(root, source);
    if (!isWithin(root, source)) {
      throw codedError(
        'EOIP_SOURCE_OUTSIDE_REPOSITORY',
        'The active file is outside eoip.repositoryRoot. Set that setting to the matching ingested repository root.',
      );
    }
    const wordRange = editor.document.getWordRangeAtPosition(editor.selection.active);
    const word = wordRange ? editor.document.getText(wordRange) : '';
    // Prefer the language server / document-symbol provider so nested symbols
    // resolve by their real name; fall back to the word at the cursor.
    let symbol = word;
    try {
      const symbols = await vscode.commands.executeDocumentSymbolProvider(editor.document.uri);
      const position = editor.selection.active;
      const enclosing = findEnclosingSymbol(symbols || [], position);
      if (enclosing) symbol = enclosing;
    } catch (_) {
      // Symbol providers are optional; word-at-cursor remains the fallback.
    }
    return {
      relativePath: normalizedPath(relative),
      symbol,
      line: editor.selection.active.line + 1,
    };
  }

  findNode(nodes, location) {
    const sameFile = nodes.filter(node =>
      normalizedPath(node.properties?.path) === location.relativePath,
    );
    if (!sameFile.length) return undefined;
    if (location.symbol) {
      const symbol = location.symbol.toLocaleLowerCase();
      return sameFile.find(node => {
        const properties = node.properties || {};
        const name = String(properties.name || '').toLocaleLowerCase();
        const qualified = String(properties.qualified_name || '').toLocaleLowerCase();
        return name === symbol || qualified === symbol || qualified.endsWith(`.${symbol}`);
      });
    }
    return sameFile
      .filter(node => Number.isInteger(Number(node.properties?.start_line)))
      .sort((left, right) =>
        Math.abs(Number(left.properties.start_line) - location.line) -
        Math.abs(Number(right.properties.start_line) - location.line),
      )[0];
  }

  contextTree(node, relativePath, impact, lineage) {
    const props = node.properties || {};
    const lineRange = props.start_line
      ? `:${props.start_line}${props.end_line && props.end_line !== props.start_line ? `-${props.end_line}` : ''}`
      : '';
    const root = this.item(
      `Current symbol: ${nodeName(node)}`,
      vscode.TreeItemCollapsibleState.Expanded,
      `${relativePath}${lineRange}`,
      node.id,
    );
    root.command = {
      command: 'eoip.openSource',
      title: 'Open Symbol Source',
      arguments: [node],
    };

    const nodes = new Map();
    for (const related of [...(impact.nodes || []), ...(lineage.nodes || [])]) {
      if (related.id !== node.id) nodes.set(related.id, related);
    }
    this.relatedCount = nodes.size;
    const edges = new Map(
      [...(impact.edges || []), ...(lineage.edges || [])].map(edge => [edge.id, edge]),
    );
    const routes = new Map();
    for (const graphPath of [...(impact.paths || []), ...(lineage.paths || [])]) {
      const terminal = graphPath.node_ids?.[graphPath.node_ids.length - 1];
      if (!terminal || routes.has(terminal)) continue;
      routes.set(
        terminal,
        (graphPath.edge_ids || []).map(edgeId => edges.get(edgeId)?.type).filter(Boolean),
      );
    }

    const grouped = new Map();
    for (const related of nodes.values()) {
      const groupName = related.label || related.domain || 'Related entities';
      if (!grouped.has(groupName)) grouped.set(groupName, []);
      const route = routes.get(related.id) || [];
      const properties = related.properties || {};
      const detail = [
        properties.path,
        properties.issue_key,
        properties.commit_sha,
        properties.source_ref,
        properties.summary,
      ].find(value => typeof value === 'string' && value.length);
      const relatedItem = this.item(
        nodeName(related),
        vscode.TreeItemCollapsibleState.None,
        route.length ? `via ${route.join(' → ')}` : undefined,
        [related.id, detail].filter(Boolean).join('\n'),
      );
      if (properties.path && Number.isInteger(Number(properties.start_line))) {
        relatedItem.command = {
          command: 'eoip.openSource',
          title: 'Open Related Source',
          arguments: [related],
        };
      }
      grouped.get(groupName).push(relatedItem);
    }

    root.children = [this.item(
      `Graph context (${nodes.size})`,
      grouped.size ? vscode.TreeItemCollapsibleState.Expanded : vscode.TreeItemCollapsibleState.None,
    )];
    root.children[0].children = [...grouped.entries()]
      .sort(([left], [right]) => left.localeCompare(right))
      .map(([label, children]) => {
        const group = this.item(
          `${label} (${children.length})`,
          vscode.TreeItemCollapsibleState.Collapsed,
        );
        group.children = children;
        return group;
      });

    const evidence = [...(impact.evidence || []), ...(lineage.evidence || [])];
    const uniqueEvidence = new Map(evidence.map(item => [
      `${item.edge_id || ''}:${item.evidence_key || ''}:${item.source_ref || ''}`,
      item,
    ]));
    this.evidenceCount = uniqueEvidence.size;
    const evidenceItems = [...uniqueEvidence.values()].map(item => this.item(
      item.evidence_key || item.source_ref || item.edge_id || 'Evidence',
      vscode.TreeItemCollapsibleState.None,
      item.source_system || undefined,
      JSON.stringify(item, null, 2),
    ));
    const evidenceGroup = this.item(
      `Provenance and evidence (${evidenceItems.length})`,
      evidenceItems.length ? vscode.TreeItemCollapsibleState.Collapsed : vscode.TreeItemCollapsibleState.None,
    );
    evidenceGroup.children = evidenceItems;
    root.children.push(evidenceGroup);
    if (impact.partial || lineage.partial) {
      root.children.push(this.item('Results are truncated by the configured traversal budget.'));
    }
    for (const warning of [...(impact.warnings || []), ...(lineage.warnings || [])]) {
      root.children.push(this.item(`Warning: ${warning}`));
    }
    return [root];
  }

  setStatus(message, preserveContext = false) {
    const status = this.item(
      this.error?.code === 'EOIP_OFFLINE' ? `Offline: ${message}` : message,
      vscode.TreeItemCollapsibleState.None,
      this.error?.code,
    );
    this.roots = preserveContext ? [status, ...this.roots] : [status];
    this.emitter.fire();
  }
}

function activate(context) {
  let selected;

  async function call(endpoint, body) {
    const token = await context.secrets.get('eoip-token');
    if (!token) {
      throw codedError('EOIP_AUTH_REQUIRED', 'Run EOIP: Set Access Token first.');
    }
    const base = vscode.workspace.getConfiguration('eoip').get('apiUrl');
    let url;
    try {
      url = new URL(endpoint, base);
    } catch (error) {
      throw codedError('EOIP_INVALID_API_URL', 'Set eoip.apiUrl to a valid HTTP or HTTPS URL.', error);
    }
    if (!['http:', 'https:'].includes(url.protocol)) {
      throw codedError('EOIP_INVALID_API_URL', 'eoip.apiUrl must use HTTP or HTTPS.');
    }
    const payload = body === undefined ? undefined : JSON.stringify(body);
    return new Promise((resolve, reject) => {
      const req = (url.protocol === 'https:' ? https : http).request(url, {
        method: payload ? 'POST' : 'GET',
        headers: {
          Authorization: `Bearer ${token}`,
          ...(payload ? {'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(payload)} : {}),
        },
        timeout: 60000,
      }, res => {
        let data = '';
        res.on('data', chunk => {
          data += chunk;
          if (Buffer.byteLength(data) > 4000000) {
            req.destroy(codedError('EOIP_RESPONSE_TOO_LARGE', 'EOIP response exceeded the 4 MB limit.'));
          }
        });
        res.on('end', () => {
          let json;
          try {
            json = JSON.parse(data);
          } catch (error) {
            reject(codedError('EOIP_INVALID_RESPONSE', 'EOIP returned an invalid JSON response.', error));
            return;
          }
          if (res.statusCode >= 400) {
            reject(codedError(
              `EOIP_HTTP_${res.statusCode}`,
              json.detail || `EOIP request failed with HTTP ${res.statusCode}.`,
            ));
            return;
          }
          resolve(json);
        });
      });
      req.on('error', error => {
        if (error.code === 'EOIP_RESPONSE_TOO_LARGE') {
          reject(error);
        } else {
          reject(codedError('EOIP_OFFLINE', 'EOIP API is unavailable. Check the local deployment and eoip.apiUrl.', error));
        }
      });
      req.on('timeout', () => req.destroy(codedError('EOIP_TIMEOUT', 'EOIP API request timed out.')));
      if (payload) req.write(payload);
      req.end();
    });
  }

  const provider = new ContextProvider(call);
  const treeView = vscode.window.createTreeView('eoip.contextView', {
    treeDataProvider: provider,
    showCollapseAll: true,
  });
  context.subscriptions.push(provider.emitter, treeView);

  // Online/offline indicator: refreshed on activation and after every call so
  // editing never depends on EOIP availability (FR-VSCODE-001 offline state).
  const statusBar = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 25);
  statusBar.command = 'eoip.search';
  context.subscriptions.push(statusBar);
  function setConnectivity(online, detail) {
    statusBar.text = online ? '$(graph) EOIP' : '$(debug-disconnect) EOIP offline';
    statusBar.tooltip = online
      ? 'EOIP API reachable. Click to search the knowledge graph.'
      : `EOIP API unavailable${detail ? `: ${detail}` : ''}. Commands stay read-only and never block editing.`;
    statusBar.backgroundColor = online ? undefined : new vscode.ThemeColor('statusBarItem.warningBackground');
    statusBar.show();
  }
  const originalCall = call;
  call = async (endpoint, body) => {
    try {
      const result = await originalCall(endpoint, body);
      setConnectivity(true);
      return result;
    } catch (error) {
      if (error.code === 'EOIP_OFFLINE' || error.code === 'EOIP_TIMEOUT') setConnectivity(false, error.message);
      throw error;
    }
  };
  provider.call = call;
  (async () => {
    try {
      await originalCall('/health/ready');
      setConnectivity(true);
    } catch (error) {
      setConnectivity(false, error.message);
    }
  })();

  async function choose(query, label) {
    const suffix = label ? `&label=${encodeURIComponent(label)}` : '';
    const result = await call(`/api/v1/search?q=${encodeURIComponent(query)}${suffix}`);
    const nodes = Array.isArray(result.nodes) ? result.nodes : [];
    const pick = await vscode.window.showQuickPick(
      nodes.map(node => ({
        label: nodeName(node),
        description: node.label,
        detail: node.id,
        node,
      })),
      {placeHolder: 'Choose an EOIP graph entity'},
    );
    if (pick) selected = pick.node;
    return pick?.node;
  }

  async function show(value) {
    const doc = await vscode.workspace.openTextDocument({
      content: JSON.stringify(value, null, 2),
      language: 'json',
    });
    await vscode.window.showTextDocument(doc, {preview: true});
  }

  function command(name, action) {
    context.subscriptions.push(vscode.commands.registerCommand(name, async (...args) => {
      try {
        return await action(...args);
      } catch (error) {
        const message = error.message || 'EOIP command failed.';
        vscode.window.showErrorMessage(message);
        return {
          ok: false,
          code: error.code || 'EOIP_COMMAND_FAILED',
          message,
        };
      }
    }));
  }

  command('eoip.setToken', async () => {
    const token = await vscode.window.showInputBox({
      prompt: 'EOIP_API_TOKEN from deploy/.env',
      password: true,
      ignoreFocusOut: true,
    });
    if (token) await context.secrets.store('eoip-token', token);
  });
  command('eoip.search', async () => {
    const query = await vscode.window.showInputBox({prompt: 'Issue key, symbol, or source path'});
    if (query) {
      const node = await choose(query);
      if (node) await show(await call(`/api/v1/entities/${encodeURIComponent(node.id)}`));
    }
  });
  command('eoip.context', async () => {
    await vscode.commands.executeCommand('workbench.view.explorer');
    const result = await provider.refresh(vscode.window.activeTextEditor);
    if (!result.ok) vscode.window.showErrorMessage(result.message);
    return result;
  });
  command('eoip.impact', async () => {
    const node = selected || provider.currentNode();
    if (!node) throw codedError('EOIP_ENTITY_REQUIRED', 'Open a source symbol or select an entity using EOIP: Search Knowledge Graph.');
    await show(await call('/api/v1/impact', {canonical_id: node.id, max_depth: 4}));
  });
  command('eoip.path', async () => {
    const target = selected || provider.currentNode();
    if (!target) throw codedError('EOIP_TARGET_REQUIRED', 'Open a source symbol or select a code entity first.');
    const sourceQuery = await vscode.window.showInputBox({
      prompt: 'Jira issue key or source canonical ID',
      placeHolder: 'For example, EOIP-1',
    });
    if (!sourceQuery) return;
    const source = await choose(sourceQuery);
    if (!source) {
      throw codedError('EOIP_SOURCE_NOT_FOUND', `No source entity matched "${sourceQuery}".`);
    }
    const [pathResult, impactResult] = await Promise.all([
      call('/api/v1/path', {source_id: source.id, target_id: target.id, max_depth: 8}),
      call('/api/v1/impact', {canonical_id: target.id, max_depth: 4}),
    ]);
    await show({source, target, path: pathResult, impact: impactResult});
  });
  command('eoip.lineage', async () => {
    const defaultId = selected?.id || provider.currentNode()?.id || '';
    const id = await vscode.window.showInputBox({prompt: 'Canonical ID to trace provenance', value: defaultId});
    if (id) await show(await call('/api/v1/lineage', {canonical_id: id, max_depth: 4}));
  });
  command('eoip.retrieval', async () => {
    const defaultId = selected?.id || provider.currentNode()?.id || '';
    const id = await vscode.window.showInputBox({prompt: 'Canonical ID', value: defaultId});
    const question = await vscode.window.showInputBox({
      prompt: 'Question',
      value: 'Explain the implementation and its evidence',
    });
    if (id && question) {
      await show(await call('/api/v1/rag', {canonical_id: id, question, synthesize: false}));
    }
  });
  command('eoip.openSource', async node => {
    const source = node || selected || provider.currentNode();
    if (!source?.properties?.path) {
      throw codedError('EOIP_SOURCE_REQUIRED', 'Select an indexed code symbol first.');
    }
    const configuredRoot = vscode.workspace.getConfiguration('eoip').get('repositoryRoot', '');
    const workspace = vscode.workspace.workspaceFolders?.[0];
    if (!configuredRoot && !workspace) {
      throw codedError('EOIP_REPOSITORY_ROOT_REQUIRED', 'Set eoip.repositoryRoot to the local ingested repository root.');
    }
    const rootPath = repositoryRoot(configuredRoot, workspace?.uri.fsPath);
    if (path.isAbsolute(source.properties.path)) {
      throw codedError('EOIP_UNSAFE_SOURCE_PATH', 'Indexed source paths must be relative to the repository root.');
    }
    const candidate = path.resolve(rootPath, source.properties.path);
    if (!isWithin(rootPath, candidate)) {
      throw codedError('EOIP_UNSAFE_SOURCE_PATH', 'Source path is outside the configured repository root.');
    }
    let realRoot;
    let realFile;
    try {
      [realRoot, realFile] = await Promise.all([fs.realpath(rootPath), fs.realpath(candidate)]);
    } catch (error) {
      throw codedError('EOIP_SOURCE_NOT_FOUND', 'The indexed source file is not present in the local repository checkout.', error);
    }
    if (!isWithin(realRoot, realFile)) {
      throw codedError('EOIP_UNSAFE_SOURCE_PATH', 'Source path resolves outside the configured repository root.');
    }

    const editor = await vscode.window.showTextDocument(
      await vscode.workspace.openTextDocument(vscode.Uri.file(realFile)),
    );
    const properties = source.properties;
    const startLine = Number.isInteger(Number(properties.start_line))
      ? Math.max(0, Number(properties.start_line) - 1)
      : 0;
    const endLine = Number.isInteger(Number(properties.end_line))
      ? Math.max(startLine, Number(properties.end_line) - 1)
      : startLine;
    const startColumn = Number.isInteger(Number(properties.start_column))
      ? Math.max(0, Number(properties.start_column))
      : 0;
    const endColumn = Number.isInteger(Number(properties.end_column))
      ? Math.max(0, Number(properties.end_column))
      : startColumn;
    const range = new vscode.Range(
      new vscode.Position(startLine, startColumn),
      new vscode.Position(endLine, endColumn),
    );
    editor.selection = new vscode.Selection(range.start, range.end);
    editor.revealRange(range, vscode.TextEditorRevealType.InCenterIfOutsideViewport);
    return {ok: true, uri: editor.document.uri.toString(), range: {
      startLine, startColumn, endLine, endColumn,
    }};
  });

  let refreshTimer;
  const scheduleRefresh = editor => {
    if (provider.containsPosition(editor)) return;
    clearTimeout(refreshTimer);
    refreshTimer = setTimeout(() => provider.refresh(editor), 350);
  };
  context.subscriptions.push(
    vscode.window.onDidChangeActiveTextEditor(scheduleRefresh),
    vscode.window.onDidChangeTextEditorSelection(event => scheduleRefresh(event.textEditor)),
  );
}

module.exports = {activate};
