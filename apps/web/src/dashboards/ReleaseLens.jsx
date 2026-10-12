import React from 'react';
import { Card, Badge, DataGrid } from '../components/ui';

export function ReleaseLens() {
  const columns = [
    { key: 'version', header: 'Release' },
    { key: 'status', header: 'Status', render: (val) => <Badge variant={val === 'DEPLOYED' ? 'success' : 'info'}>{val}</Badge> },
    { key: 'author', header: 'Author' },
    { key: 'deployedAt', header: 'Deployed At' },
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <Card
        title="Release & Version Tracking Lens"
        subtitle="Deployment governance, artifact verification hashes, and service release timelines"
      >
        <DataGrid columns={columns} data={[]} title="Recent Deployment Milestones" />
      </Card>
    </div>
  );
}
export default ReleaseLens;
