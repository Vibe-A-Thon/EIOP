import React from 'react';
import { Card, Badge, DataGrid } from '../components/ui';

export function ChangeLens() {
  const columns = [
    { key: 'changeId', header: 'Change ID' },
    { key: 'entity', header: 'Entity' },
    { key: 'kind', header: 'Type', render: (val) => <Badge variant={val === 'ADD' ? 'success' : 'warning'}>{val}</Badge> },
    { key: 'timestamp', header: 'Timestamp' },
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <Card
        title="Graph Mutation & Change Diff Lens"
        subtitle="Auditable log of entity modifications, relationship additions, and schema alterations"
      >
        <DataGrid columns={columns} data={[]} title="Recent Graph Mutations" />
      </Card>
    </div>
  );
}
export default ChangeLens;
