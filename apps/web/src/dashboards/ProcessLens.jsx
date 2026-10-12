import React from 'react';
import { Card, Badge } from '../components/ui';

export function ProcessLens() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <Card
        title="Workflow Execution & Process Mining Lens"
        subtitle="Monitors business workflows, step durations, and architectural process deviations"
      >
        <p style={{ color: '#94a3b8', fontSize: '0.9rem' }}>
          Real-time monitoring of harness workflows, causal graphs, and operational tasks.
        </p>
      </Card>
    </div>
  );
}
export default ProcessLens;
