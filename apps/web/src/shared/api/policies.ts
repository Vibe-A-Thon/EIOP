/** JSON is valid YAML and preserves every server policy field and condition. */
export function policyDocument(statements: readonly unknown[]): string {
  return JSON.stringify({policies: statements}, null, 2) + '\n';
}
