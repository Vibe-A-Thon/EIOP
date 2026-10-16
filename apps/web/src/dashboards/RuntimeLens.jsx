import React from 'react';
import { Card, Badge, Button } from '../components/ui';

export function RuntimeLens() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <Card
        title="Runtime Metrics & Agent Fleet Activity"
        subtitle="Live telemetry across active loops, memory graphs, and token budgets"
      >
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginTop: '16px' }}>
          <div style={{ padding: '16px', background: 'rgba(255,255,255,0.03)', borderRadius: '8px' }}>
            <span style={{ color: '#94a3b8', fontSize: '0.8rem' }}>Active Agents</span>
            <h2 style={{ margin: '8px 0', color: '#6366f1' }}>14</h2>
            <Badge variant="success">All Healthy</Badge>
          </div>
          <div style={{ padding: '16px', background: 'rgba(255,255,255,0.03)', borderRadius: '8px' }}>
            <span style={{ color: '#94a3b8', fontSize: '0.8rem' }}>Token Budget Util</span>
            <h2 style={{ margin: '8px 0', color: '#06b6d4' }}>42.3%</h2>
            <Badge variant="info">Within Quota</Badge>
          </div>
          <div style={{ padding: '16px', background: 'rgba(255,255,255,0.03)', borderRadius: '8px' }}>
            <span style={{ color: '#94a3b8', fontSize: '0.8rem' }}>Circuit Breaker</span>
            <h2 style={{ margin: '8px 0', color: '#10b981' }}>CLOSED</h2>
            <Badge variant="success">Normal Execution</Badge>
          </div>
        </div>
      </Card>
    </div>
  );
}
export default RuntimeLens;
