const assert = require('node:assert/strict');
const vscode = require('vscode');

async function run({symbol, requests, document}) {
  let invocations = 0;
  let flatSymbols = false;
  const registration = vscode.languages.registerDocumentSymbolProvider(
    {scheme: 'file', pattern: '**/sample.py'},
    {provideDocumentSymbols() {
      invocations += 1;
      if (flatSymbols) {
        return [new vscode.SymbolInformation('target', vscode.SymbolKind.Function, 'sample',
          new vscode.Location(document.uri, new vscode.Range(0, 0, 1, 12)))];
      }
      const child = new vscode.DocumentSymbol(
        'target', '', vscode.SymbolKind.Function,
        new vscode.Range(0, 0, 1, 12), new vscode.Range(0, 4, 0, 10),
      );
      const parent = new vscode.DocumentSymbol('sample', '', vscode.SymbolKind.Module,
        new vscode.Range(0, 0, 1, 12), new vscode.Range(0, 0, 0, 3));
      parent.children = [child];
      return [parent];
    }},
  );
  try {
    const editor = await vscode.window.showTextDocument(document);
    editor.selection = new vscode.Selection(1, 5, 1, 5);
    const result = await vscode.commands.executeCommand('eoip.context');
    assert.equal(result.ok, true);
    assert.equal(result.node.id, symbol.id);
    assert.ok(invocations > 0, 'must invoke the real VS Code document-symbol command');
    const searches = requests.filter(item => item.url.startsWith('/api/v1/search'));
    assert.equal(new URL(searches.at(-1).url, 'http://localhost').searchParams.get('q'), 'target',
      'cursor in function body must use enclosing symbol, not the word "return"');
    assert.equal(document.isDirty, false);
    flatSymbols = true;
    const flatResult = await vscode.commands.executeCommand('eoip.context');
    assert.equal(flatResult.ok, true, 'flat SymbolInformation must resolve through its location range');
    assert.equal(flatResult.node.id, symbol.id);
  } finally {
    registration.dispose();
  }
}

module.exports = {run};
