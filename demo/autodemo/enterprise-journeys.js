const {randomUUID} = require('node:crypto');

function requireResult(condition, message) {
  if (!condition) throw new Error(message);
}

function enterpriseJourneys(api, anchor, runId = randomUUID()) {
  const subject = `urn:eoip:demo:truth:${runId}`;
  const graph = 'graph:northstar-commerce';
  const workId = anchor.startsWith('urn:') ? anchor : `urn:eoip:work:item:jira:${anchor}`;
  return [
    ['Federation: route a typed query and inspect execution', async () => {
      const sources = await api('/api/v1/federation/sources');
      requireResult(sources.sources?.length > 0, 'Federation has no registered sources');
      const result = await api('/api/v1/federation/query', {entity_types: ['WorkItem']});
      requireResult(result.row_count > 0 && result.plan?.fragments?.some(item => item.status === 'executed'),
        'Federation returned no rows or executed fragments');
      return {sources, result, boundary: 'Local graph adapters; not proof of remote credentialed federation'};
    }],
    ['Truth: preserve conflicting claims, resolve authority and explain', async () => {
      const claims = [];
      for (const [suffix, value, authority] of [['primary', 'Commerce SRE', 0.9], ['secondary', 'Legacy operations', 0.4]]) {
        claims.push(await api('/api/v1/truth/claims', {
          claim_id: `${subject}:${suffix}`, subject_id: subject, predicate: 'owner', value,
          source_id: `urn:eoip:demo:source:${suffix}`, source_authority: authority, extraction_confidence: 0.9,
        }));
      }
      const resolution = await api('/api/v1/truth/resolve',
        {subject_id: subject, predicate: 'owner', policy: 'highest-authority'});
      requireResult(resolution.chosen_claim_id === `${subject}:primary`, 'Truth selected the wrong authority');
      const assertion = await api(`/api/v1/truth/assertions/${subject}/owner`);
      requireResult(assertion.value === 'Commerce SRE', 'Resolved assertion did not round trip');
      const explanation = await api(`/api/v1/truth/explain/${subject}/owner`);
      requireResult(explanation.explanation?.includes('highest authority'), 'Resolution explanation is missing');
      return {claims, resolution, assertion, explanation,
        boundary: 'Isolated synthetic claims in process memory; not persisted in Hubble or across API restart'};
    }],
    ['Query template: save, bind, explain cost and remove only this demo template', async () => {
      const template = await api('/api/v1/query/templates',
        {name: `client-demo-${runId}`, intent: 'SEARCH', anchor_params: ['key']});
      requireResult(template.template_id, 'Template identifier missing');
      try {
        const plan = await api(`/api/v1/query/templates/${template.template_id}/bind`, {params: {key: anchor}});
        requireResult(plan.anchors?.[0] === anchor, 'Template bound the wrong anchor');
        const explanation = await api('/api/v1/query/explain', plan);
        requireResult(explanation.steps?.length > 0, 'Query explanation is empty');
        const cost = await api('/api/v1/query/cost', plan);
        requireResult(Number.isFinite(cost.score) && cost.score >= 0 && cost.score <= 1, 'Query cost is invalid');
        return {template, plan, explanation, cost, boundary: 'Estimated cost; not a measured latency promise'};
      } finally {
        await api(`/api/v1/query/templates/${template.template_id}`, undefined, undefined, {method: 'DELETE'});
      }
    }],
    ['Retrieval: faceted identity and keyword evidence trace', async () => {
      const search = await api('/api/v1/search/faceted', {query: 'checkout'});
      requireResult(search.total > 0 && search.hits?.every(hit => hit.canonical_id), 'Faceted search has no identified hits');
      const retrieval = await api('/api/v1/retrieval/search', {question: 'checkout', strategy: 'keyword', top_k: 5});
      requireResult(retrieval.strategy === 'keyword' && retrieval.trace?.steps?.length > 0 &&
        retrieval.evidence_refs?.length > 0, 'Retrieval has no traceable evidence');
      return {search, retrieval};
    }],
    ['Graph assertions: prove connected work and visibly report an expected violation', async () => {
      const passing = await api('/api/v1/graph-tests/run', {
        id: `client-demo-pass-${runId}`, assertions: [
          {id: 'work-connected', type: 'cardinality', label: 'WorkItem', filters: {canonical_id: workId}, min_count: 1},
        ],
      });
      requireResult(passing.conformant === true && passing.failed === 0, 'Seeded graph assertion failed');
      const expectedFailure = await api('/api/v1/graph-tests/run', {
        id: `client-demo-negative-${runId}`, assertions: [
          {id: 'expected-zero-connections', type: 'cardinality', label: 'WorkItem',
            filters: {canonical_id: workId}, max_count: 0},
        ],
      });
      requireResult(expectedFailure.conformant === false && expectedFailure.failed === 1,
        'Expected graph violation was not reported');
      return {passing, expected_violation: expectedFailure,
        boundary: 'The deliberate violation is read-only and expected; actual failures still stop the demo'};
    }],
    ['Taxonomy: create synthetic concepts, relate them and validate the scheme', async () => {
      const scheme = await api('/api/v1/taxonomy/schemes',
        {title: `Client demo commerce ${runId}`, description: 'Synthetic in-process demonstration'});
      requireResult(scheme.scheme_id, 'Taxonomy scheme identifier missing');
      const concepts = [];
      for (const label of ['Checkout resilience', 'Release assurance']) {
        concepts.push(await api('/api/v1/taxonomy/concepts', {scheme_id: scheme.scheme_id, pref_label: label}));
      }
      const mapping = await api('/api/v1/taxonomy/mappings', {
        source_id: concepts[0].concept_id, target_id: concepts[1].concept_id, kind: 'relatedMatch',
      });
      const readBack = await api(`/api/v1/taxonomy/concepts?scheme=${encodeURIComponent(scheme.scheme_id)}`);
      requireResult(readBack.concepts?.length === 2, 'Taxonomy concepts did not round trip');
      const validation = await api(`/api/v1/taxonomy/validate?scheme=${encodeURIComponent(scheme.scheme_id)}`);
      requireResult(validation.label_conflicts?.length === 0, 'Synthetic taxonomy has label conflicts');
      return {scheme, concepts, mapping, validation,
        boundary: 'SKOS state is process-local, not persisted in Hubble'};
    }],
    ['Knowledge product: lifecycle, persisted read-back and lineage', async () => {
      const product = await api('/api/v1/catalog/products', {
        name: `Synthetic Northstar assurance ${runId}`, owner: 'client-demo', domain: 'engineering',
        source_graphs: [graph], consumers: ['demo:release-assurance'],
      });
      requireResult(product.state === 'Draft' && product.product_id, 'Product was not created as Draft');
      const history = [];
      for (const state of ['Experimental', 'Trusted', 'Certified']) {
        const transition = await api(`/api/v1/catalog/products/${product.product_id}/transition`, {to_state: state});
        requireResult(transition.state === state, `Product did not transition to ${state}`);
        history.push(transition);
      }
      const readBack = await api(`/api/v1/catalog/products/${product.product_id}`);
      requireResult(readBack.state === 'Certified' && readBack.name === product.name, 'Product read-back mismatch');
      const lineage = await api(`/api/v1/catalog/products/${product.product_id}/lineage`);
      requireResult(lineage.source_graphs?.some(item => item.source_graph === graph) &&
        lineage.consumers?.some(item => item.consumer === 'demo:release-assurance'), 'Product lineage mismatch');
      return {product, history, readBack, lineage,
        boundary: 'Persisted synthetic KnowledgeProduct; Certified is a lifecycle label, not external certification'};
    }],
    ['Simple query languages: enterprise data and ontology types', async () => {
      const rows = await api('/api/v1/query/language', {language: 'eoql', query: 'SELECT * FROM WorkItem LIMIT 5'});
      requireResult(rows.count > 0 && rows.results?.every(item => item.canonical_id), 'EOQL returned no identified data');
      const types = await api('/api/v1/query/language', {language: 'osql', query: 'LIST TYPES'});
      requireResult(types.types?.includes('WorkItem'), 'OSQL did not expose the WorkItem type');
      return {rows, types};
    }],
  ];
}

module.exports = {enterpriseJourneys, requireResult};
