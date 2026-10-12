import React from 'react';
import { Card, Button, Badge } from '../components/ui';

export function SimulationLens() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <Card
        title="What-If Scenario Simulation Lens"
        subtitle="Simulates outage blast radiuses, cascading service failures, and policy changes"
      >
        <div style={{ display: 'flex', gap: '12px', marginTop: '12px' }}>
          <Button variant="primary" ariaLabel="Simulate Database Outage">
            Run DB Outage Simulation
          </Button>
          <Button variant="secondary" ariaLabel="Simulate Network Partition">
            Run AZ Partition Simulation
          </Button>
        </div>
      </Card>
    </div>
  );
}
export default SimulationLens;
