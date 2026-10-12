import React, { useState } from 'react';
import { Card, Badge, Button, Input, DataGrid } from '../components/ui';

export function SearchAnalyticsDashboard() {
  const [synonymTerm, setSynonymTerm] = useState('');
  const [synonymTarget, setSynonymTarget] = useState('');

  const topQueryColumns = [
    { key: 'query', header: 'Search Query' },
    { key: 'count', header: 'Frequency' },
    { key: 'ctr', header: 'Click-Through Rate', render: (val) => `${(val * 100).toFixed(1)}%` },
    { key: 'latency', header: 'Avg Latency (ms)', render: (val) => `${val} ms` },
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <Card
        title="Search Intelligence & Relevance Tuning Dashboard"
        subtitle="Analyze query traffic, identify zero-result searches, and tune ranking weights"
      >
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px', marginBottom: '24px' }}>
          <div style={{ padding: '16px', background: 'rgba(255,255,255,0.03)', borderRadius: '8px' }}>
            <span style={{ color: '#94a3b8', fontSize: '0.8rem' }}>Total Searches</span>
            <h2 style={{ margin: '8px 0', color: '#f8fafc' }}>24,890</h2>
            <Badge variant="info">+12% vs last week</Badge>
          </div>
          <div style={{ padding: '16px', background: 'rgba(255,255,255,0.03)', borderRadius: '8px' }}>
            <span style={{ color: '#94a3b8', fontSize: '0.8rem' }}>Zero-Result Rate</span>
            <h2 style={{ margin: '8px 0', color: '#10b981' }}>1.4%</h2>
            <Badge variant="success">Optimal (&lt; 2%)</Badge>
          </div>
          <div style={{ padding: '16px', background: 'rgba(255,255,255,0.03)', borderRadius: '8px' }}>
            <span style={{ color: '#94a3b8', fontSize: '0.8rem' }}>Avg Query Latency</span>
            <h2 style={{ margin: '8px 0', color: '#6366f1' }}>14.2 ms</h2>
            <Badge variant="info">Fast</Badge>
          </div>
          <div style={{ padding: '16px', background: 'rgba(255,255,255,0.03)', borderRadius: '8px' }}>
            <span style={{ color: '#94a3b8', fontSize: '0.8rem' }}>Click-Through Rate</span>
            <h2 style={{ margin: '8px 0', color: '#06b6d4' }}>78.5%</h2>
            <Badge variant="success">High Intent Match</Badge>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
          <div>
            <h4 style={{ color: '#f8fafc', marginBottom: '12px' }}>Configure Synonyms &amp; Term Boosts</h4>
            <div style={{ display: 'flex', gap: '8px', marginBottom: '12px' }}>
              <Input
                placeholder="Source term (e.g. auth)"
                value={synonymTerm}
                onChange={(e) => setSynonymTerm(e.target.value)}
                ariaLabel="Synonym source term"
                style={{ flex: 1, marginBottom: 0 }}
              />
              <Input
                placeholder="Target synonym (e.g. login)"
                value={synonymTarget}
                onChange={(e) => setSynonymTarget(e.target.value)}
                ariaLabel="Synonym target synonym"
                style={{ flex: 1, marginBottom: 0 }}
              />
              <Button size="md" variant="primary">Add Synonym</Button>
            </div>
          </div>
          <div>
            <h4 style={{ color: '#f8fafc', marginBottom: '12px' }}>A/B Ranking Experiments</h4>
            <div style={{ display: 'flex', gap: '12px' }}>
              <Button variant="secondary">Experiment A: BM25 + Vector</Button>
              <Button variant="secondary">Experiment B: Hybrid Causal Graph</Button>
            </div>
          </div>
        </div>
      </Card>

      <DataGrid columns={topQueryColumns} data={[]} title="Top Query Volume & Relevance Health" />
    </div>
  );
}
export default SearchAnalyticsDashboard;
